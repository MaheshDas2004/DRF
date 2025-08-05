import django_filters
from .models import Employee

class CustomEmployeeFilter(django_filters.FilterSet):
    # id=django_filters.RangeFilter(field_name='id')

    id_min=django_filters.CharFilter(method='filter_by_id_range',label='from_emp_id')
    id_max=django_filters.CharFilter(method='filter_by_id_range',label='to_emp_id')


    emp_name=django_filters.CharFilter(field_name='emp_name',lookup_expr='iexact')
    designation=django_filters.CharFilter(field_name='designation',lookup_expr='iexact')#this will accept case insensitive also
    class Meta:
        model=Employee
        fields=['designation','emp_name','id_min','id_max']
    
    def filter_by_id_range(self,queryset,name,value):
        if name=='id_min':
            return queryset.filter(emp_id__gte=value)
        elif name=='id_max':
            return queryset.filter(emp_id__lte=value)
        return queryset 