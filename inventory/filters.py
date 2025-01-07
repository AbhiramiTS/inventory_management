import django_filters
from .models import Product, Supplier

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Product Name')
    description = django_filters.CharFilter(lookup_expr='icontains', label='Description')
    category = django_filters.CharFilter(lookup_expr='icontains', label='Category')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')
    stock_qty_min = django_filters.NumberFilter(field_name='stock_qty', lookup_expr='gte', label='Min Stock')
    stock_qty_max = django_filters.NumberFilter(field_name='stock_qty', lookup_expr='lte', label='Max Stock')
    supplier = django_filters.ModelChoiceFilter(queryset=Supplier.objects.all(), label='Supplier')

    class Meta:
        model = Product
        fields = ['name', 'category', 'price_min', 'price_max', 'stock_qty_min', 'stock_qty_max', 'supplier']
