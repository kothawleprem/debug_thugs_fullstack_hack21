import django_filters
from . models import *
from django_filters import CharFilter

class SlotFilter(django_filters.FilterSet):
    state = CharFilter(field_name='state',lookup_expr='icontains')
    city = CharFilter(field_name='city',lookup_expr='icontains')
    class Meta:
        model = Slot
        fields = ['city','state']

class PincodeFilter(django_filters.FilterSet):
    state = CharFilter(field_name='state',lookup_expr='icontains')
    city = CharFilter(field_name='city',lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['city','state']
   