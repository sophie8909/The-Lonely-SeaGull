# =============================================================================
# services.py
# =============================================================================
# @AUTHOR: Ting-Hsuan Lien, Jung Shiao
# @VERSION: X.0
# @DATE: latest edit - 23.03.2025
#
# @PURPOSE: Services used for the Users, CustomerData and OwnerData
# =======================================================

# Import the necessary libraries
import json
from typing import List, Optional

# Local libraries
from models.models import User


# In-memory store simulation
class UsersService:
    """ CRUD operations for users, only get_user method
        is used in the project
    """

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
    
class CustomerControllerDataService:
    """ Methods to return a print in the console with some details about the customer data """

    shopping_cart = None
    current_person = None
    person_count = None

    @classmethod
    def __str__(cls):
        return f"Person count: {cls.person_count}, Current person: {cls.current_person}, Shopping cart: {cls.shopping_cart}"
    
    @classmethod
    def __repr__(cls):
        return cls.__str__()