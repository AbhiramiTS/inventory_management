from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        if self.quantity > self.product.stock_qty:
            raise ValueError("Insufficient stock for this sale.")
        if self.status == 'Completed':
            self.product.stock_qty -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Incoming Stock'),
        ('out', 'Outgoing Stock'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    movement_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.movement_type == 'in':
            self.product.stock_qty += self.quantity
        elif self.movement_type == 'out':
            if self.quantity > self.product.stock_qty:
                raise ValueError("Insufficient stock for the movement.")
            self.product.stock_qty -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)
