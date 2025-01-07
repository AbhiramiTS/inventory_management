from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProductForm, SupplierForm, SalesOrderForm, StockMovementForm
from .models import Product, Supplier
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . models import *
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from .models import Supplier, Product, SalesOrder
from datetime import datetime, timedelta

from datetime import datetime, timedelta
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from .filters import ProductFilter


def dashboard(request):
    try:
        # Ensure there are records in each table
        suppliers = Supplier.objects.all()
        products = Product.objects.all()
        sales_orders = SalesOrder.objects.all()

        # Safe checks for empty result sets
        total_sales_orders = sales_orders.count() if sales_orders.exists() else 0
        total_products = products.count() if products.exists() else 0
        total_suppliers = suppliers.count() if suppliers.exists() else 0

        total_sales_value = sales_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
        out_of_stock_count = products.filter(stock_qty=0).count() if products.exists() else 0
        pending_orders_count = sales_orders.filter(status='Pending').count() if sales_orders.exists() else 0

        context = {
            'suppliers': suppliers,
            'products': products,
            'total_sales_orders': total_sales_orders,
            'sales_orders': sales_orders,
            'total_products': total_products,
            'total_suppliers': total_suppliers,
            'total_sales_value': total_sales_value,
            'out_of_stock_count': out_of_stock_count,
            'pending_orders_count': pending_orders_count,
        }

        return render(request, 'inventory/dashboard.html', context)

    except ObjectDoesNotExist:
        messages.error(request, 'Some data could not be fetched. Please try again later.')
        return render(request, 'inventory/dashboard.html', {})



def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Supplier added successfully!')
                return redirect('list_suppliers')
            except Exception as e:
                messages.error(request, f"Error adding supplier: {str(e)}")
        else:
            messages.error(request, 'There was an error with the provided data. Please check the form.')
    else:
        form = SupplierForm()

    return render(request, 'inventory/add_supplier.html', {'form': form})


def supplier_detail(request, id):
    try:
        supplier = get_object_or_404(Supplier, pk=id)
        supplier_products = supplier.products.all()
        total_products = supplier_products.count()
        return render(request, 'inventory/supplier_detail.html', {
            'supplier': supplier,
            'supplier_products': supplier_products,
            'total_products': total_products
        })
    except Exception as e:
        messages.error(request, f"Error fetching supplier details: {str(e)}")
        return render(request, 'inventory/supplier_detail.html', {})


def list_suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/list_suppliers.html', {'suppliers': suppliers})


def update_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    form = SupplierForm(instance=supplier)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()  # Save the updated supplier
            return redirect('supplier', id=supplier.id)  # Correct the URL here
        else:
            messages.error(request, 'There was an error with the provided data.')

    context = {'form': form, 'supplier_id': id}
    return render(request, 'inventory/supplier_form.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if Product.objects.filter(name=name).exists():  # Ensure no duplicate product
                messages.error(request, 'A product with this name already exists.')
            else:
                form.save()
                messages.success(request, 'Product added successfully!')
                return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'form': form})

# List Products View
def list_products(request):
    products = Product.objects.select_related('supplier').all()
    product_filter = ProductFilter(request.GET, queryset=products)
    return render(request, 'inventory/list_products.html', {'products': products, 'filter':product_filter})

# Edit Product View
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/edit_product.html', {'form': form, 'product': product})

# Delete Product View
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('list_products')


def add_stock_movement(request):
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock movement added successfully.')
            return redirect('add_stock_movement')
    else:
        form = StockMovementForm()
    return render(request, 'inventory/add_stock_movement.html', {'form': form})


def create_sale_order(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            product = order.product
            if order.quantity > product.stock_qty:
                messages.error(request, 'Insufficient stock for this product.')
            else:
                order.total_price = order.quantity * product.price
                order.status = 'Pending'
                order.save()
                messages.success(request, 'Sale order created successfully.')
                return redirect('create_sale_order')
    else:
        form = SalesOrderForm()
    return render(request, 'inventory/create_sale_order.html', {'form': form})


def save(self, *args, **kwargs):
    if self.status == 'Cancelled' and self.pk:  # Ensure this is an update
        original = SalesOrder.objects.get(pk=self.pk)
        if original.status != 'Cancelled':  # Prevent multiple cancellations
            self.product.stock_qty += self.quantity
            self.product.save()
    super().save(*args, **kwargs)
    
    
def cancel_sale_order(request, order_id):
    order = get_object_or_404(SalesOrder, id=order_id)
    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        order.product.stock_qty += order.quantity
        order.product.save()
        order.save()
        messages.success(request, 'Sale order cancelled successfully.')
    else:
        messages.error(request, 'Sale order is already cancelled.')
    return redirect('list_sale_orders')



def complete_sale_order(request, order_id):
    order = get_object_or_404(SalesOrder, id=order_id)
    if order.status == 'Pending':
        order.status = 'Completed'
        order.save()
        messages.success(request, 'Sale order completed successfully.')
    else:
        messages.error(request, 'Sale order cannot be completed.')
    return redirect('list_sale_orders')



def list_sale_orders(request):
    orders = SalesOrder.objects.all()
    return render(request, 'inventory/list_sale_orders.html', {'orders': orders})



def stock_level_check(request):
    products = Product.objects.all()
    return render(request, 'inventory/stock_level_check.html', {'products': products})




