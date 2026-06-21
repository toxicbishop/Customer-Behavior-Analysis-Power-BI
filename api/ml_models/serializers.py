from rest_framework import serializers

class SegmentInputSerializer(serializers.Serializer):
    # Define input fields for segmentation
    # Example: age = serializers.IntegerField()
    pass

class PurchasePredictionInputSerializer(serializers.Serializer):
    # Define input fields for purchase prediction
    pass

class ChurnPredictionInputSerializer(serializers.Serializer):
    # Define input fields for churn prediction
    pass

class RecommenderInputSerializer(serializers.Serializer):
    # Define input fields for recommender
    pass
