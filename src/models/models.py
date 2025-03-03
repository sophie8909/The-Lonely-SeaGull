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
    nr: Optional[str] = None
    articleid: Optional[str] = None
    articletype: Optional[str] = None
    name: str = ""
    name2: Optional[str] = None
    priceinclvat: float = 0.0
    volumeml: Optional[int] = None
    priceperlitre: Optional[float] = None
    introduced: Optional[date] = None
    finaldelivery: Optional[date] = None
    category: Optional[str] = None
    packaging: Optional[str] = None
    captype: Optional[str] = None
    countryoforigin: Optional[str] = None
    countryoforiginlandname: Optional[str] = None
    producer: Optional[str] = None
    provider: Optional[str] = None
    productionyear: Optional[str] = None
    testedproductionyear: Optional[str] = None
    alcoholstrength: Optional[float] = None
    module: Optional[str] = None
    assortment: Optional[str] = None
    organic: bool = False
    kosher: bool = False
    order_items: List = field(default_factory=list)
    beers_sold: List = field(default_factory=list)

@dataclass
class BeerSold:
    transaction_id: int
    user_id: int
    beer_id: int
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Payment:
    transaction_id: int
    user_id: int
    admin_id: int
    amount: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class VipCustomer:
    user_id: int
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
    beer_id: int
    quantity: int = 0
    price: float = 0.0

