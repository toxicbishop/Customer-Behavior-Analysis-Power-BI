from django.urls import path
from .views import SegmentView, PurchasePredictionView, ChurnPredictionView, RecommenderView

urlpatterns = [
    path('segment/', SegmentView.as_view(), name='segment'),
    path('predict/', PurchasePredictionView.as_view(), name='predict'),
    path('churn/', ChurnPredictionView.as_view(), name='churn'),
    path('recommend/', RecommenderView.as_view(), name='recommend'),
]
