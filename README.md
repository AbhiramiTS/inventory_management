# Inventory Management System


## Features Included

### Dashboard
- The dashboard provides key metrics like:
  - Products out of stock
  - Total orders
  - Delivered orders
  - Pending orders

### Product List
- View and filter products based on different criteria such as:
  - Name
  - Category
  - Price range
  - Stock quantity
  - Supplier

### Suppliers
- Manage supplier information and view the list of products supplied by each supplier.

### Sales Orders
- View and manage sales orders, update their status, and view their details.

### Add Supplier
- Validates and saves supplier details, ensuring no duplicate entries for email or phone.

### List Suppliers
- Displays a paginated list of all suppliers in the database.

### Add Product
- Includes validation to prevent duplicate product entries based on the name.

### List Products
- Displays all products along with supplier details.

### Edit Product
- Allows editing of product details.

### Delete Product
- Enables deletion of a product.

### Product Filter
You can filter products using the `ProductFilter` form available on the product list page. The following filters are available:
  - **Name**: Search by product name (case-insensitive)
  - **Category**: Search by product category (case-insensitive)
  - **Price Range**: Filter products by price range (min and max)
  - **Stock Quantity**: Filter products by stock quantity (min and max)
  - **Supplier**: Filter products by supplier

### Add Stock Movement
- Record incoming stock ("in") or outgoing stock ("out") and update the stock levels accordingly.
- Ensure proper validation of stock levels (e.g., no negative stock).

### Create Sale Order
- Allow users to create sale orders by selecting products, verifying sufficient stock, and calculating the total price.
- Ensure that the stock levels are updated correctly after each sale.

### Cancel Sale Order
- Cancel an existing sale order ensuring that the status is set to "Cancelled" and stock is updated back if the sale is canceled.

### Complete Sale Order
- Mark an order as "Completed" and update the stock levels accordingly.
- Ensure the sale is valid and the status is updated to "Completed".

### List Sale Orders
- Retrieve a list of all sale orders, including the product name, quantity, total price, sale date, status, and any additional notes.

### Stock Level Check
- Implement a function to check and return the current stock level for each product.

