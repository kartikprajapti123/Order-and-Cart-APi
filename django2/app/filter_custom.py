from django_filters.rest_framework import FilterSet
from app.models import product
class customfil(FilterSet):
    class Meta:
        model=product
        
        fields={
            'name':['exact'],
            'price':['lt','gt'],
            
        }