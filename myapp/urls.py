from django.urls import path
from . import views

app_name = "myapp"

urlpatterns = [
    path("", views.getchatresponse, name="chat_response")
]
