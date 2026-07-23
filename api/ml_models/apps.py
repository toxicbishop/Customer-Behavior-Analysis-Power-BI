import joblib
import os
from django.apps import AppConfig

# Module-level registry — loaded once, shared across all requests
MODELS = {}

MODEL_PATHS = {
    "churn":    "ml/models/churn_rf_model.pkl",
    "segment":  "ml/models/segmentation_model.pkl",
    "purchase": "ml/models/purchase_model.pkl",
    "recommend":"ml/models/recommender_model.pkl",
}


class MlModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ml_models"

    def ready(self):
        """
        Called once when Django starts. Loads every available model into the
        MODELS dict. Missing models log a warning instead of crashing the
        server — endpoints handle the None case gracefully.
        """
        import logging
        logger = logging.getLogger(__name__)

        for key, path in MODEL_PATHS.items():
            if os.path.exists(path):
                try:
                    MODELS[key] = joblib.load(path)
                    logger.info(f"[ml_models] Loaded '{key}' model from {path}")
                except Exception as e:
                    logger.error(f"[ml_models] Failed to load '{key}' model: {e}")
                    MODELS[key] = None
            else:
                logger.warning(
                    f"[ml_models] Model not found: {path}. "
                    f"Run the training script first: python ml/train_{key}.py"
                )
                MODELS[key] = None