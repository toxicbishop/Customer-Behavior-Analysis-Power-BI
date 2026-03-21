import pandas as pd
import mlflow
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import RandomForestClassifier
# XGBoost and collaborative filtering will be imported as needed

# --- Data Loading ---
def load_data():
    import os
    # Get the directory where THIS file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up 2 levels and into the data/raw folder
    data_path = os.path.join(current_dir, '..', '..', 'data', 'raw', 'customer_shopping_behavior.csv')
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    return df

# --- Feature Engineering ---
def preprocess_data(df):
    # Example: scale numeric columns, encode categorical
    scaler = StandardScaler()
    # TODO: Select numeric columns
    # df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    # TODO: Encode categorical columns
    # df[categorical_cols] = LabelEncoder().fit_transform(df[categorical_cols])
    # TODO: Imputation if needed
    return df

# --- Model Training Stubs ---
def train_segmentation(df):
    with mlflow.start_run(run_name="Segmentation"):
        # KMeans example
        mlflow.set_tag("model_type", "KMeans")
        # TODO: Add KMeans training code
        mlflow.log_param("n_clusters", 4)
        # mlflow.log_metric("segmentation_score", score)
        # DBSCAN example
        mlflow.set_tag("model_type", "DBSCAN")
        # TODO: Add DBSCAN training code
        # mlflow.log_param("eps", 0.5)
        # mlflow.log_metric("dbscan_score", score)

def train_purchase_prediction(df):
    with mlflow.start_run(run_name="PurchasePrediction"):
        mlflow.set_tag("model_type", "XGBoost")
        # TODO: Add XGBoost training code
        # mlflow.log_param("max_depth", 6)
        # mlflow.log_metric("accuracy", acc)

def train_churn_prediction(df):
    with mlflow.start_run(run_name="ChurnPrediction"):
        mlflow.set_tag("model_type", "RandomForest")
        # TODO: Add Random Forest training code
        # mlflow.log_param("n_estimators", 100)
        # mlflow.log_metric("roc_auc", auc)

def train_recommender(df):
    with mlflow.start_run(run_name="Recommender"):
        mlflow.set_tag("model_type", "CollaborativeFiltering")
        # TODO: Add collaborative filtering training code
        # mlflow.log_param("method", "ALS")
        # mlflow.log_metric("recommendation_score", score)
