from typing import List, Optional
import json
from models.models import User, Beer, Order, OrderItem, Payment, VipCustomer, BeerSold

# In-memory store simulation

class UsersService:
    _users: List[User] = []
    _data_path = ''
    @classmethod
    def __init__(cls, file_path) -> None:
        cls._data_path = file_path
        cls.load_users()
    @classmethod
    def load_users(cls) -> None:
        with open(cls._data_path, 'r') as f:
            data = json.load(f)
            for user_data in data:
                user = User(**user_data)
                cls.add_user(user)

    @classmethod
    def save_users(cls, json_path: str) -> None:
        data = [user.__dict__ for user in cls._users]
        with open(json_path, 'w') as f:
            json.dump(data, f)

    @classmethod
    def get_users(cls) -> List[User]:
        return cls._users
    
    @classmethod
    def get_user(cls, username: str) -> Optional[User]:
        for user in cls._users:
            if user.username == username:
                return user
        return None

    @classmethod
    def add_user(cls, user: User) -> None:
        cls._users.append(user)

    @classmethod
    def set_user(cls, user: User) -> bool:
        for idx, existing in enumerate(cls._users):
            if existing.user_id == user.user_id:
                cls._users[idx] = user
                return True
        return False

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        for idx, existing in enumerate(cls._users):
            if existing.user_id == user_id:
                cls._users.pop(idx)
                return True
        return False

class BeersService:
    _beers: List[Beer] = []

    @classmethod
    def get_beers(cls) -> List[Beer]:
        return cls._beers

    @classmethod
    def add_beer(cls, beer: Beer) -> None:
        cls._beers.append(beer)

    @classmethod
    def set_beer(cls, beer: Beer) -> bool:
        for idx, existing in enumerate(cls._beers):
            if existing.beer_id == beer.beer_id:
                cls._beers[idx] = beer
                return True
        return False

    @classmethod
    def delete_beer(cls, beer_id: int) -> bool:
        for idx, existing in enumerate(cls._beers):
            if existing.beer_id == beer_id:
                cls._beers.pop(idx)
                return True
        return False

class OrdersService:
    _orders: List[Order] = []

    @classmethod
    def get_orders(cls) -> List[Order]:
        return cls._orders

    @classmethod
    def add_order(cls, order: Order) -> None:
        cls._orders.append(order)

    @classmethod
    def update_order(cls, order: Order) -> bool:
        for idx, existing in enumerate(cls._orders):
            if existing.order_id == order.order_id:
                cls._orders[idx] = order
                return True
        return False

    @classmethod
    def delete_order(cls, order_id: int) -> bool:
        for idx, existing in enumerate(cls._orders):
            if existing.order_id == order_id:
                cls._orders.pop(idx)
                return True
        return False

class PaymentsService:
    _payments: List[Payment] = []

    @classmethod
    def get_payments(cls) -> List[Payment]:
        return cls._payments

    @classmethod
    def add_payment(cls, payment: Payment) -> None:
        cls._payments.append(payment)

    @classmethod
    def delete_payment(cls, transaction_id: int) -> bool:
        for idx, existing in enumerate(cls._payments):
            if existing.transaction_id == transaction_id:
                cls._payments.pop(idx)
                return True
        return False

class VipCustomersService:
    _vip_customers: List[VipCustomer] = []

    @classmethod
    def get_vip_customers(cls) -> List[VipCustomer]:
        return cls._vip_customers

    @classmethod
    def add_vip_customer(cls, vip: VipCustomer) -> None:
        cls._vip_customers.append(vip)

    @classmethod
    def set_vip_customer(cls, vip: VipCustomer) -> bool:
        for idx, existing in enumerate(cls._vip_customers):
            if existing.user_id == vip.user_id:
                cls._vip_customers[idx] = vip
                return True
        return False

    @classmethod
    def delete_vip_customer(cls, user_id: int) -> bool:
        for idx, existing in enumerate(cls._vip_customers):
            if existing.user_id == user_id:
                cls._vip_customers.pop(idx)
                return True
        return False

class BeerSoldService:
    _beer_solds: List[BeerSold] = []

    @classmethod
    def get_beer_solds(cls) -> List[BeerSold]:
        return cls._beer_solds

    @classmethod
    def add_beer_sold(cls, beer_sold: BeerSold) -> None:
        cls._beer_solds.append(beer_sold)

    @classmethod
    def delete_beer_sold(cls, transaction_id: int) -> bool:
        for idx, existing in enumerate(cls._beer_solds):
            if existing.transaction_id == transaction_id:
                cls._beer_solds.pop(idx)
                return True
        return False
