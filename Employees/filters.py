import django_filters
from .models import Employee

class CustomEmployeeFilter(django_filters.FilterSet):
    id=django_filters.RangeFilter(field_name='id')
    emp_name=django_filters.CharFilter(field_name='emp_name',lookup_expr='iexact')
    designation=django_filters.CharFilter(field_name='designation',lookup_expr='iexact')#this will accept case insensitive also
    class Meta:
        model=Employee
        fields=['designation','emp_name','id']