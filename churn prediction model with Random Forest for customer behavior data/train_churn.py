"""
Churn Prediction — Random Forest
Customer Behavior Analysis Project

Dataset: customer_shopping_behavior.csv
  Expected columns (standard Kaggle shopping trends dataset):
    Customer ID, Age, Gender, Item Purchased, Category,
    Purchase Amount (USD), Location, Size, Color, Season,
    Review Rating, Subscription Status, Shipping Type,
    Discount Applied, Promo Code Used, Previous Purchases,
    Payment Method, Frequency of Purchases

  NOTE: There is no native "Churn" label in this dataset.
  We engineer it from behavioral signals (see engineer_churn_label).
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    ConfusionMatrixDisplay,
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib
import os
import warnings

warnings.filterwarnings("ignore")

# ─── Config ──────────────────────────────────────────────────────────────────
DATA_PATH = "data/customer_shopping_behavior.csv"
MODEL_OUTPUT_PATH = "models/churn_rf_model.pkl"
MLFLOW_EXPERIMENT = "churn_prediction"
RANDOM_STATE = 42

# ─── 1. Load Data ─────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[load]  shape: {df.shape}")
    print(f"[load]  columns: {df.columns.tolist()}")
    print(f"[load]  nulls:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    return df


# ─── 2. Engineer Churn Label ──────────────────────────────────────────────────
# Strategy:
#   The dataset has no explicit churn column, so we define churn as a customer
#   who shows at least 2 of the following 3 disengagement signals:
#     - Low purchase frequency  : "Annually" or "Quarterly"
#     - Low previous purchases  : below the 30th percentile
#     - Poor review rating      : below 3.0
#   This is a business-logic label — document it clearly in your README.
def engineer_churn_label(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    freq_map = {
        "Weekly": 0,
        "Fortnightly": 0,
        "Monthly": 0,
        "Bi-Weekly": 0,
        "Quarterly": 1,
        "Annually": 1,
        "Every 3 Months": 1,
    }
    df["low_freq"] = df["Frequency of Purchases"].map(freq_map).fillna(0).astype(int)

    prev_threshold = df["Previous Purchases"].quantile(0.30)
    df["low_prev_purchases"] = (df["Previous Purchases"] <= prev_threshold).astype(int)

    df["low_rating"] = (df["Review Rating"] < 3.0).astype(int)

    # Churn = 2 or more signals
    df["churn_signals"] = df["low_freq"] + df["low_prev_purchases"] + df["low_rating"]
    df["Churn"] = (df["churn_signals"] >= 2).astype(int)

    churn_rate = df["Churn"].mean()
    print(f"[label] churn rate: {churn_rate:.2%}  (target: 20–40% is healthy)")
    print(f"[label] class distribution:\n{df['Churn'].value_counts()}")

    return df


# ─── 3. Preprocess ────────────────────────────────────────────────────────────
CATEGORICAL_COLS = [
    "Gender",
    "Category",
    "Location",
    "Season",
    "Subscription Status",
    "Shipping Type",
    "Discount Applied",
    "Promo Code Used",
    "Payment Method",
    "Size",
]

NUMERICAL_COLS = [
    "Age",
    "Purchase Amount (USD)",
    "Review Rating",
    "Previous Purchases",
]

# Columns to drop before training
DROP_COLS = [
    "Customer ID",
    "Item Purchased",
    "Color",
    "Frequency of Purchases",  # used to engineer label — drop to prevent leakage
    "low_freq",
    "low_prev_purchases",
    "low_rating",
    "churn_signals",
]


def preprocess(df: pd.DataFrame):
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    # Final column lists (only keep what's actually in the dataframe)
    num_cols = [c for c in NUMERICAL_COLS if c in X.columns]
    cat_cols = [c for c in CATEGORICAL_COLS if c in X.columns]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    print(f"[split] train: {X_train.shape}  test: {X_test.shape}")
    return X_train, X_test, y_train, y_test, preprocessor


# ─── 4. Build Pipeline ────────────────────────────────────────────────────────
def build_pipeline(preprocessor) -> Pipeline:
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",   # important: handles class imbalance automatically
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    return Pipeline([("preprocessor", preprocessor), ("classifier", rf)])


# ─── 5. Evaluate ──────────────────────────────────────────────────────────────
def evaluate(pipeline, X_test, y_test) -> dict:
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]

    report = classification_report(y_test, y_pred, output_dict=True)
    roc_auc = roc_auc_score(y_test, y_prob)

    print("\n[eval] Classification Report:")
    print(classification_report(y_test, y_pred))
    print(f"[eval] ROC-AUC: {roc_auc:.4f}")

    metrics = {
        "accuracy": report["accuracy"],
        "precision_churn": report["1"]["precision"],
        "recall_churn": report["1"]["recall"],
        "f1_churn": report["1"]["f1-score"],
        "roc_auc": roc_auc,
    }
    return metrics, y_pred, y_prob


# ─── 6. Plot & Save Artifacts ─────────────────────────────────────────────────
def save_artifacts(pipeline, X_test, y_test, y_pred, y_prob):
    os.makedirs("artifacts", exist_ok=True)

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(6, 5))
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Retained", "Churned"])
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title("Confusion Matrix — Churn Prediction")
    plt.tight_layout()
    plt.savefig("artifacts/confusion_matrix.png", dpi=150)
    plt.close()

    # ROC curve
    fig, ax = plt.subplots(figsize=(6, 5))
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    ax.plot(fpr, tpr, label=f"ROC-AUC = {auc:.3f}", color="#534AB7", linewidth=2)
    ax.plot([0, 1], [0, 1], "--", color="gray", linewidth=1)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve — Churn Prediction")
    ax.legend()
    plt.tight_layout()
    plt.savefig("artifacts/roc_curve.png", dpi=150)
    plt.close()

    # Feature importance (top 20)
    rf_model = pipeline.named_steps["classifier"]
    preprocessor = pipeline.named_steps["preprocessor"]

    # Reconstruct feature names after one-hot encoding
    num_features = preprocessor.transformers_[0][2]
    ohe = preprocessor.transformers_[1][1]
    cat_features = ohe.get_feature_names_out(preprocessor.transformers_[1][2]).tolist()
    all_features = list(num_features) + cat_features

    importances = rf_model.feature_importances_
    feat_df = (
        pd.DataFrame({"feature": all_features, "importance": importances})
        .sort_values("importance", ascending=False)
        .head(20)
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=feat_df, x="importance", y="feature", ax=ax, color="#534AB7")
    ax.set_title("Top 20 Feature Importances — Random Forest")
    ax.set_xlabel("Importance")
    plt.tight_layout()
    plt.savefig("artifacts/feature_importance.png", dpi=150)
    plt.close()

    print("[artifacts] Saved: confusion_matrix.png, roc_curve.png, feature_importance.png")
    return feat_df


# ─── 7. MLflow Run ────────────────────────────────────────────────────────────
def train_with_mlflow():
    mlflow.set_experiment(MLFLOW_EXPERIMENT)

    df = load_data(DATA_PATH)
    df = engineer_churn_label(df)
    X_train, X_test, y_train, y_test, preprocessor = preprocess(df)
    pipeline = build_pipeline(preprocessor)

    # Cross-validation before final fit
    print("\n[cv]  Running 5-fold cross-validation...")
    cv_scores = cross_val_score(
        pipeline, X_train, y_train,
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
        scoring="roc_auc",
        n_jobs=-1,
    )
    print(f"[cv]  CV ROC-AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    with mlflow.start_run(run_name="churn_random_forest"):
        # Log hyperparameters
        rf_params = pipeline.named_steps["classifier"].get_params()
        mlflow.log_params({
            "n_estimators": rf_params["n_estimators"],
            "max_depth": rf_params["max_depth"],
            "min_samples_split": rf_params["min_samples_split"],
            "min_samples_leaf": rf_params["min_samples_leaf"],
            "class_weight": str(rf_params["class_weight"]),
            "churn_label_strategy": "2_of_3_signals",
            "test_size": 0.2,
        })

        # Fit on full training set
        pipeline.fit(X_train, y_train)

        # Evaluate
        metrics, y_pred, y_prob = evaluate(pipeline, X_test, y_test)

        # Log metrics
        mlflow.log_metrics({
            **metrics,
            "cv_roc_auc_mean": cv_scores.mean(),
            "cv_roc_auc_std": cv_scores.std(),
        })

        # Save and log artifacts
        feat_df = save_artifacts(pipeline, X_test, y_test, y_pred, y_prob)
        mlflow.log_artifact("artifacts/confusion_matrix.png")
        mlflow.log_artifact("artifacts/roc_curve.png")
        mlflow.log_artifact("artifacts/feature_importance.png")

        # Log model to MLflow registry
        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="churn_model",
            registered_model_name="CustomerChurnRF",
            input_example=X_test.iloc[:5],
        )

        # Save local copy for FastAPI
        os.makedirs("models", exist_ok=True)
        joblib.dump(pipeline, MODEL_OUTPUT_PATH)
        print(f"\n[mlflow] Model saved locally: {MODEL_OUTPUT_PATH}")
        print(f"[mlflow] Run ID: {mlflow.active_run().info.run_id}")

    return pipeline, feat_df


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    pipeline, feat_df = train_with_mlflow()
    print("\n[done] Top 10 features driving churn:")
    print(feat_df.head(10).to_string(index=False))
