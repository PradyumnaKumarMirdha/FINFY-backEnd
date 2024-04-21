# urls.py

from django.urls import path
from .views import ScrapingView

urlpatterns = [
    path('stock-detail/', ScrapingView.as_view(), name='stock_detail'),
]
