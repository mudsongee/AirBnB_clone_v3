#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        
        # Hash the password when creating or updating a user object
        if kwargs.get("password"):
            self.password = hashlib.md5(kwargs["password"].encode()).hexdigest()

    def to_dict(self, **kwargs):
        """Returns a dictionary containing all keys/values of the instance"""
        # Call the parent class's to_dict() method
        dictionary = super().to_dict(**kwargs)

        # Exclude the 'password' key from the dictionary except for FileStorage
        if getenv("HBNB_TYPE_STORAGE") != "file":
            dictionary.pop("password", None)

        return dictionary