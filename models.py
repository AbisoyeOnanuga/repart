# models.py
from . import db

# Create your models here.

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    condition = db.Column(db.String(20))
    price = db.Column(db.Numeric(10, 2))
    seller_info = db.Column(db.String(100))
    purchase_options = db.Column(db.String(20))
    link = db.Column(db.String(500))
    shipping = db.Column(db.String(50))
    location = db.Column(db.String(50))
    quantity_sold = db.Column(db.String(50))

    def __repr__(self):
        return f"<Product {self.title}>"

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f"<Customer {self.name}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    customer = db.relationship("Customer", backref="orders")
    date_ordered = db.Column(db.DateTime, default=db.func.now())
    complete = db.Column(db.Boolean, default=False)
    transaction_id = db.Column(db.String(200))

    def __repr__(self):
        return f"<Order {self.id}>"

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product", backref="order_items")
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    order = db.relationship("Order", backref="order_items")
    quantity = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f"<OrderItem {self.product.title}>"
