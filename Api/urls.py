from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

# for using viewset
router=DefaultRouter()
router.register('employees',views.EmployeeViewSet,basename='employee')

urlpatterns = [
    # Api Endpoints
    path('students/',views.studentsView),
    path('students/<int:id>/',views.single_studentsView),

    # path('Employees/',views.Employees.as_view()),#class based views
    # path('Employees/<int:pk>/',views.Single_Employee.as_view())#class based views
    path('',include(router.urls))
]
