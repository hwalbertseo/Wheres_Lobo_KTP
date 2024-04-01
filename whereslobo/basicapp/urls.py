from django.urls import path, include
from basicapp import views

urlpatterns = [
    path("", views.index),
    path("home/", views.index)
]
