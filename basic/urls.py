from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tmp_test/", views.temp_test, name="temp_test"),
    path("email/", views.test_email, name="test_email"),
    path("email/send", views.test_send_email, name="send_email"),
]


