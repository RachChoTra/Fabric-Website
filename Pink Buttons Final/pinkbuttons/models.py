from . import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price_per_meter = db.Column(db.Float, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(60), nullable=False, default='defaultfabric.jpg')

    def __repr__(self):
        str = "Id: {}, Name: {}, PricePerMeter: {}, QuanityInStock: {}, Image: {}\n" 
        str = str.format( self.id, self.name, self.price_per_meter, self.quantity_in_stock, self.image)
        return str

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    total_price = db.Column(db.Float, nullable=False)
    items = db.relationship('Order_Details', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id} by {self.customer_name}>'

class Order_Details(db.Model):
    __tablename__ = 'order_details'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_meter = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref='order_items')

    def __repr__(self):
        return f'<OrderItem {self.id} - {self.quantity} of {self.product.name}>'
