from crm.models import Customer, Product, Order
from django.utils import timezone

# Clear old data
Order.objects.all().delete()
Customer.objects.all().delete()
Product.objects.all().delete()

# Create customers
alice = Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
bob = Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")
carol = Customer.objects.create(name="Carol", email="carol@example.com")

# Create products
laptop = Product.objects.create(name="Laptop", price=999.99, stock=10)
mouse = Product.objects.create(name="Mouse", price=25.50, stock=100)
keyboard = Product.objects.create(name="Keyboard", price=45.00, stock=50)

# Create an order
order = Order.objects.create(
    customer=alice,
    total_amount=laptop.price + mouse.price,
    order_date=timezone.now()
)
order.products.set([laptop, mouse])

print("Database seeded successfully.")
