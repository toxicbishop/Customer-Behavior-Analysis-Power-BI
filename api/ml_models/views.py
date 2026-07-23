import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .apps import MODELS
from .serializers import (
    ChurnInputSerializer,
    SegmentInputSerializer,
    PurchaseInputSerializer,
    RecommendInputSerializer,
)


def _model_unavailable(name):
    return Response(
        {
            "error": f"'{name}' model is not loaded. "
                     f"Run ml/train_{name}.py first to generate the model file."
        },
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


# ─── Churn Prediction ─────────────────────────────────────────────────────────

class ChurnPredictionView(APIView):
    def post(self, request):
        serializer = ChurnInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model = MODELS.get("churn")
        if model is None:
            return _model_unavailable("churn")

        d = serializer.validated_data
        input_df = pd.DataFrame([{
            "Age":                   d["age"],
            "Gender":                d["gender"],
            "Category":              d["category"],
            "Purchase Amount (USD)": d["purchase_amount_usd"],
            "Location":              d["location"],
            "Size":                  d["size"],
            "Season":                d["season"],
            "Review Rating":         d["review_rating"],
            "Subscription Status":   d["subscription_status"],
            "Shipping Type":         d["shipping_type"],
            "Discount Applied":      d["discount_applied"],
            "Promo Code Used":       d["promo_code_used"],
            "Previous Purchases":    d["previous_purchases"],
            "Payment Method":        d["payment_method"],
        }])

        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])

        if probability < 0.35:
            risk_level = "Low"
            recommendation = "Customer is stable. Continue standard engagement."
        elif probability < 0.65:
            risk_level = "Medium"
            recommendation = "Send targeted retention offer or loyalty incentive."
        else:
            risk_level = "High"
            recommendation = "Immediate outreach required. High churn risk detected."

        return Response({
            "churn_prediction":  prediction,           # 0 = retained, 1 = churned
            "churn_probability": round(probability, 4),
            "risk_level":        risk_level,
            "recommendation":    recommendation,
        }, status=status.HTTP_200_OK)


# ─── Segmentation ─────────────────────────────────────────────────────────────

class SegmentView(APIView):
    def post(self, request):
        serializer = SegmentInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model = MODELS.get("segment")
        if model is None:
            return _model_unavailable("segment")

        d = serializer.validated_data
        input_df = pd.DataFrame([{
            "Age":                   d["age"],
            "Purchase Amount (USD)": d["purchase_amount_usd"],
            "Review Rating":         d["review_rating"],
            "Previous Purchases":    d["previous_purchases"],
            "Gender":                d["gender"],
            "Category":              d["category"],
            "Season":                d["season"],
        }])

        segment = int(model.predict(input_df)[0])
        return Response({
            "segment_id":  segment,
            "description": f"Customer assigned to segment {segment}.",
        }, status=status.HTTP_200_OK)


# ─── Purchase Prediction ──────────────────────────────────────────────────────

class PurchasePredictionView(APIView):
    def post(self, request):
        serializer = PurchaseInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model = MODELS.get("purchase")
        if model is None:
            return _model_unavailable("purchase")

        d = serializer.validated_data
        input_df = pd.DataFrame([{
            "Age":                   d["age"],
            "Gender":                d["gender"],
            "Category":              d["category"],
            "Purchase Amount (USD)": d["purchase_amount_usd"],
            "Location":              d["location"],
            "Season":                d["season"],
            "Review Rating":         d["review_rating"],
            "Subscription Status":   d["subscription_status"],
            "Discount Applied":      d["discount_applied"],
            "Promo Code Used":       d["promo_code_used"],
            "Previous Purchases":    d["previous_purchases"],
            "Payment Method":        d["payment_method"],
        }])

        prediction = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])
        return Response({
            "will_purchase":        prediction,
            "purchase_probability": round(probability, 4),
        }, status=status.HTTP_200_OK)


# ─── Recommender ──────────────────────────────────────────────────────────────

class RecommenderView(APIView):
    def post(self, request):
        serializer = RecommendInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        model = MODELS.get("recommend")
        if model is None:
            return _model_unavailable("recommend")

        d = serializer.validated_data
        # Collaborative filtering models expose a get_recommendations() style interface.
        # Adjust the call below to match your actual recommender's API.
        recommendations = model.get_recommendations(
            customer_id=d["customer_id"],
            n=d["top_n"],
        )
        return Response({
            "customer_id":     d["customer_id"],
            "recommendations": recommendations,
        }, status=status.HTTP_200_OK)