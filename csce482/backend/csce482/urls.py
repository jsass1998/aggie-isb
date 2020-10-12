from django.conf.urls import include, url  # noqa
from django.urls import path
from django.shortcuts import redirect
from django.contrib import admin
admin.autodiscover()

from . import views

# Example of defining API endpoints as URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", lambda request : redirect("exampleapp/")),
    path("api/helloworld/", views.HelloWorldView.as_view(), name='hello_world'),
    path("api/create_question/", views.create_question, name='create_question'),
    path("api/exampleapp/", include('exampleapp.urls')) # include routes in other 'apps' - keep routes with relevant code
]
