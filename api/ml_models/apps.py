import os
import logging
import joblib # pyright: ignore[reportMissingImports]
from django.apps import AppConfig # pyright: ignore[reportMissingModuleSource]
from django.conf import settings # pyright: ignore[reportMissingModuleSource]

# Module-level registry — loaded once, shared across all requests
MODELS = {}

logger = logging.getLogger(__name__)


class MlModelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ml_models"

    def ready(self):
        """
        Called once when Django starts. Loads every available model into the
        MODELS dict. Paths are resolved relative to the project root (one
        level above settings.BASE_DIR's manage.py, i.e. api/../ml/models),
        NOT relative to whatever directory the server was launched from.
        """
        # settings.BASE_DIR is the 'api/' folder (where manage.py lives).
        # The 'ml/' folder sits one level up, at the repo root.
        project_root = os.path.dirname(settings.BASE_DIR)

        model_paths = {
            "churn":     os.path.join(project_root, "ml", "models", "churn_rf_model.pkl"),
            "segment":   os.path.join(project_root, "ml", "models", "segmentation_model.pkl"),
            "purchase":  os.path.join(project_root, "ml", "models", "purchase_model.pkl"),
            "recommend": os.path.join(project_root, "ml", "models", "recommender_model.pkl"),
        }

        for key, path in model_paths.items():
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