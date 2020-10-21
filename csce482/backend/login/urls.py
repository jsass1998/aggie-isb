from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.GoogleLogin.as_view(), name='google_login'),
]