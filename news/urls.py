from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.get_news_data, name='scrape_data'),
    # Other URL patterns for your Django project
]
