from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import mlflow
from .ml_pipeline import (
    load_data,
    preprocess_data,
    train_segmentation,
    train_purchase_prediction,
    train_churn_prediction,
    train_recommender
)

class SegmentView(APIView):
    def post(self, request):
        df = load_data()
        df = preprocess_data(df)
        train_segmentation(df)
        return Response({"segment": "segmentation complete"}, status=status.HTTP_200_OK)

class PurchasePredictionView(APIView):
    def post(self, request):
        df = load_data()
        df = preprocess_data(df)
        train_purchase_prediction(df)
        return Response({"prediction": "purchase prediction complete"}, status=status.HTTP_200_OK)

class ChurnPredictionView(APIView):
    def post(self, request):
        df = load_data()
        df = preprocess_data(df)
        train_churn_prediction(df)
        return Response({"churn": "churn prediction complete"}, status=status.HTTP_200_OK)

class RecommenderView(APIView):
    def post(self, request):
        df = load_data()
        df = preprocess_data(df)
        train_recommender(df)
        return Response({"recommendation": "recommendation complete"}, status=status.HTTP_200_OK)
