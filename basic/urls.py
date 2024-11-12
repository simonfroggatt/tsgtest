from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tmp_test/", views.temp_test, name="temp_test"),
]
