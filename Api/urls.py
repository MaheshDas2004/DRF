from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    # Api Endpoints
    path('students/',views.studentsView),
    path('students/<int:id>/',views.single_studentsView),
]
