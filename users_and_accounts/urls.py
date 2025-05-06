from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path("register", views.register_request, name="register"),
    re_path(r'^edit/$', views.edit, name='edit'),
    path('validate_username/', views.validate_username, name='validate_username'),
    path('contact/', views.contact_form_view, name='contact_form'),
    path('book/toggle_like/', views.toggle_like_book, name='toggle_like_book'),

]