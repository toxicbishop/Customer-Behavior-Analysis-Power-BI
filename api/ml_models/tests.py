from django.test import TestCase
from .ml_pipeline import load_data, preprocess_data

class PipelineTests(TestCase):
    def test_load_data(self):
        df = load_data()
        self.assertIsNotNone(df)

    def test_preprocess_data(self):
        df = load_data()
        df_processed = preprocess_data(df)
        self.assertIsNotNone(df_processed)

# Add more tests for model training and API endpoints
