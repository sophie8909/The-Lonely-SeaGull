from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional

@dataclass
class User:
    user_id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str = ""
    phone: Optional[str] = None
    credentials: int = 0
    password: str = ""

@dataclass
class Beer:
    beer_id: int
    name: str
    producer: str
    country: str
    beer_type: str
    strength: float
    serving_size: str = "tap" # values: tap, bottle
    price: float = 0.0
    picture: Optional[str] = None

@dataclass
class Product:
    product_id: int
    name: str
    price: float = 0.0
    picture: Optional[str] = None

@dataclass
class Wine(Product):
    year: int = 0
    producer: str = ""
    grape: str = ""
    serving_size: str = "glass" # values: glass, bottle

@dataclass
class Cocktail(Product):
    strength: float = 0.0
    contents: List[str] = field(default_factory=list)

@dataclass
class Food(Product):
    ingredients: List[str] = field(default_factory=list)

@dataclass
class ProductSold:
    transaction_id: int
    user_id: int
    product_id: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Payment:
    transaction_id: int
    user_id: int
    admin_id: int
    amount: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class VipCustomer(User):
    credit_limit: float = 0.0

@dataclass
class Order:
    order_id: int
    user_id: int
    status: str = "pending"  # values: pending, completed, canceled
    created_at: datetime = field(default_factory=datetime.utcnow)
    order_items: List = field(default_factory=list)

@dataclass
class OrderItem:
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int = 0
    price: float = 0.0

