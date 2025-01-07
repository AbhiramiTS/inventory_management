import random
from datetime import date
from faker import Faker
import os
import django

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory_management.settings")
django.setup()

# Import models after setting up Django
from inventory.models import Supplier, Product, SalesOrder, StockMovement

# Your logic here
print("Filling data...")


fake = Faker()

# Create 5 Suppliers
for _ in range(5):
    supplier = Supplier.objects.create(
        name=fake.company(),
        email=fake.company_email(),
        phone=fake.phone_number(),
        address=fake.address(),
    )

# Create 20 Products
for _ in range(20):
    supplier = random.choice(Supplier.objects.all())  # Randomly select a supplier
    product = Product.objects.create(
        name=fake.word(),
        description=fake.text(),
        category=fake.word(),
        price=random.uniform(10, 100),
        stock_qty=random.randint(50, 200),  # Random stock between 50 and 200
        supplier=supplier
    )

# Create 20 Sales Orders
for _ in range(20):
    product = random.choice(Product.objects.all())  # Randomly select a product
    quantity = random.randint(1, 5)  # Random quantity between 1 and 5
    total_price = product.price * quantity
    SalesOrder.objects.create(
        product=product,
        quantity=quantity,
        total_price=total_price,
        sale_date=fake.date_this_year(),
        status=random.choice(['Pending', 'Completed', 'Cancelled']),
    )

# Create 20 Stock Movements
for _ in range(20):
    product = random.choice(Product.objects.all())  # Randomly select a product
    movement_type = random.choice(['in', 'out'])
    quantity = random.randint(1, 50)  # Random quantity between 1 and 50
    StockMovement.objects.create(
        product=product,
        quantity=quantity,
        movement_type=movement_type,
        movement_date=fake.date_this_year(),
        notes=fake.text()
    )

print("Random data has been created successfully.")
