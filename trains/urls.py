from django.urls import path
from .views import TrainSearchView, TrainCreateUpdateView

urlpatterns = [
    path("trains/search/", TrainSearchView.as_view(), name="train-search"),
    path("trains/", TrainCreateUpdateView.as_view(), name="train-create-update"),
]
