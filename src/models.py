from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    credentials = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # orders = db.relationship('Order', backref='user', lazy=True)
    # ...existing relationships if needed...

class Beer(db.Model):
    __tablename__ = 'beers'
    beer_id = db.Column(db.Integer, primary_key=True)
    nr = db.Column(db.String(10))
    articleid = db.Column(db.String(10))
    articletype = db.Column(db.String(10))
    name = db.Column(db.String(100), nullable=False)
    name2 = db.Column(db.String(100))
    priceinclvat = db.Column(db.Numeric(10,2), nullable=False)
    volumeml = db.Column(db.Integer)
    priceperlitre = db.Column(db.Numeric(10,2))
    introduced = db.Column(db.Date)
    finaldelivery = db.Column(db.Date)
    category = db.Column(db.String(50))
    packaging = db.Column(db.String(50))
    captype = db.Column(db.String(50))
    countryoforigin = db.Column(db.String(100))
    countryoforiginlandname = db.Column(db.String(100))
    producer = db.Column(db.String(100))
    provider = db.Column(db.String(100))
    productionyear = db.Column(db.String(4))
    testedproductionyear = db.Column(db.String(4))
    alcoholstrength = db.Column(db.Numeric(5,2))
    module = db.Column(db.String(50))
    assortment = db.Column(db.String(50))
    organic = db.Column(db.Boolean, default=False)
    kosher = db.Column(db.Boolean, default=False)
    order_items = db.relationship('OrderItem', backref='beer', lazy=True)
    beers_sold = db.relationship('BeerSold', backref='beer', lazy=True)

class BeerSold(db.Model):
    __tablename__ = 'beers_sold'
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    beer_id = db.Column(db.Integer, db.ForeignKey('beers.beer_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class VipCustomer(db.Model):
    __tablename__ = 'vip_customers'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    credit_limit = db.Column(db.Numeric(10,2), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(Enum('pending', 'completed', 'canceled', name='order_status'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    beer_id = db.Column(db.Integer, db.ForeignKey('beers.beer_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)

