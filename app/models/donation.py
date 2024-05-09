from app.models.base import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, Text


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)