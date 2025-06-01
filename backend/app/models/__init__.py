# This file makes the 'models' directory a Python package.

from .user import UserInDB, UserCreate, UserPublic, UserRole, UserUpdate # Added UserUpdate
from .gym import GymInDB, GymCreate, GymPublic, GymUpdate # Added GymUpdate
from .subscription import SubscriptionInDB, SubscriptionCreate
from .physical_data import PhysicalDataBase as PhysicalData
# If PhysicalDataInDB is distinct and needed for direct DB ops, import it too.
# from .physical_data import PhysicalDataInDB

# It's good practice to define __all__ if you want to control what `from .models import *` imports
__all__ = [
    "UserInDB",
    "UserCreate",
    "UserPublic",
    "UserRole",
    "UserUpdate", # Added UserUpdate
    "GymInDB",
    "GymCreate",
    "GymPublic",
    "GymUpdate", # Added GymUpdate
    "SubscriptionInDB",
    "SubscriptionCreate",
    "PhysicalData", # Or PhysicalDataBase if you prefer that name
]

# Note: The gym.py model is assumed to exist based on the original instructions.
# If it doesn't exist, those lines related to Gym will cause an ImportError.
# For this task, I'm including them as per the prompt's example.
