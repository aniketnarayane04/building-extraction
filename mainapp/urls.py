from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.input, name="input"),
    path('output', views.output, name="output")
]

