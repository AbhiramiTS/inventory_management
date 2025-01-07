from django import forms
from .models import Product, Supplier, StockMovement, SalesOrder

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Supplier Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Address',
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_qty', 'supplier']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Product Name',
            'description': 'Description',
            'category': 'Category',
            'price': 'Price',
            'stock_qty': 'Stock Quantity',
            'supplier': 'Supplier',
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        
        
class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['product', 'quantity']
