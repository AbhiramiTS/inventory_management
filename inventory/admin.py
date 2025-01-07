from django.contrib import admin
from .models import Supplier, Product, SalesOrder, StockMovement

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(SalesOrder)
admin.site.register(StockMovement)
