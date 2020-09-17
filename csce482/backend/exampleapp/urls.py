from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'exampleapp'
urlpatterns = [
    path('', lambda request : redirect('helloworld/')),
    path('helloworld/', views.HelloWorldView.as_view(), name='hello_world'),
]
