#!/usr/bin/python3
""" holds class Review"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

class Review(BaseModel, Base):
    """Review class handles all application reviews"""
    if STORAGE_TYPE == "db":
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        place = relationship('Place', back_populates='reviews')
        user = relationship('User', back_populates='reviews')
    else:
        place_id = ''
        user_id = ''
        text = ''
