from dataclasses import dataclass
from typing import Optional, List


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
    balance: float = 0.0

@dataclass
class CustomerControllerData:
    person_count: int
    current_person: int
    shopping_cart: List[List[dict]]

@dataclass
class OwnerData:
    cart: List[dict]
