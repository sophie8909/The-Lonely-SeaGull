# =============================================================================
# models.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Yuxie Liu
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Data models for the Users, CustomerData and OwnerData
# =======================================================

# Import the necessary libraries
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class User:
    """ Class representing a user """
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
    """ Class representing a customer data """
    person_count: int
    current_person: int
    shopping_cart: List[List[dict]]

@dataclass
class OwnerData:
    """ Class representing owner data """
    cart: List[dict]
