from django.urls import path
from stockdata.views import ScrapingView

urlpatterns = [
    path('scrape/', ScrapingView.as_view(), name='scrape_data'),
    # Other URL patterns for your Django project
]
