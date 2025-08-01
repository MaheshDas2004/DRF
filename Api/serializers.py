from rest_framework import serializers
from students.models import Students
from Employees.models import Employee
class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model=Students
        fields="__all__"
class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model=Employee
        fields="__all__"