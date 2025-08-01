from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    # Api Endpoints
    path('students/',views.studentsView),
    path('students/<int:id>/',views.single_studentsView),

    path('Employees/',views.Employees.as_view()),#class based views
    path('Employees/<int:id>/',views.Single_Employee.as_view())#class based views
]
