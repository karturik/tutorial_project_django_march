from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("register", views.register_request, name="register"),
    re_path(r'^edit/$', views.edit, name='edit'),
]