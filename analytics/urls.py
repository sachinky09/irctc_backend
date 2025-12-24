from django.urls import path
from .views import TopRoutesView

urlpatterns = [
    path("analytics/top-routes/", TopRoutesView.as_view(), name="top-routes"),
]
