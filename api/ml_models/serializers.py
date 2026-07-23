from rest_framework import serializers


class ChurnInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=18, max_value=100)
    gender = serializers.ChoiceField(choices=["Male", "Female"])
    category = serializers.CharField()
    purchase_amount_usd = serializers.FloatField(min_value=0)
    location = serializers.CharField()
    size = serializers.CharField()
    season = serializers.ChoiceField(choices=["Spring", "Summer", "Fall", "Winter"])
    review_rating = serializers.FloatField(min_value=1.0, max_value=5.0)
    subscription_status = serializers.ChoiceField(choices=["Yes", "No"])
    shipping_type = serializers.CharField()
    discount_applied = serializers.ChoiceField(choices=["Yes", "No"])
    promo_code_used = serializers.ChoiceField(choices=["Yes", "No"])
    previous_purchases = serializers.IntegerField(min_value=0)
    payment_method = serializers.CharField()


class SegmentInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=18, max_value=100)
    purchase_amount_usd = serializers.FloatField(min_value=0)
    review_rating = serializers.FloatField(min_value=1.0, max_value=5.0)
    previous_purchases = serializers.IntegerField(min_value=0)
    gender = serializers.ChoiceField(choices=["Male", "Female"])
    category = serializers.CharField()
    season = serializers.ChoiceField(choices=["Spring", "Summer", "Fall", "Winter"])


class PurchaseInputSerializer(serializers.Serializer):
    age = serializers.IntegerField(min_value=18, max_value=100)
    gender = serializers.ChoiceField(choices=["Male", "Female"])
    category = serializers.CharField()
    purchase_amount_usd = serializers.FloatField(min_value=0)
    location = serializers.CharField()
    season = serializers.ChoiceField(choices=["Spring", "Summer", "Fall", "Winter"])
    review_rating = serializers.FloatField(min_value=1.0, max_value=5.0)
    subscription_status = serializers.ChoiceField(choices=["Yes", "No"])
    discount_applied = serializers.ChoiceField(choices=["Yes", "No"])
    promo_code_used = serializers.ChoiceField(choices=["Yes", "No"])
    previous_purchases = serializers.IntegerField(min_value=0)
    payment_method = serializers.CharField()


class RecommendInputSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(min_value=1)
    top_n = serializers.IntegerField(min_value=1, max_value=20, default=5)