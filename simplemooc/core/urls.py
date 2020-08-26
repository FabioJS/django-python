from django.contrib import admin
from django.urls import path, include, re_path
from simplemooc.core import views

urlpatterns = [
    re_path(r'^contato/', views.contact, name='contact'),
    re_path(r'^', views.home, name='home'),
]
