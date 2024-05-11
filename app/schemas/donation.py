from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import AbstractBaseSchema


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]


class DonationCreate(DonationBase):
    id: Optional[int]
    create_date: Optional[datetime]


class DonationDB(DonationBase, AbstractBaseSchema):
    user_id: int


class DonationUserDB(DonationCreate):
    pass

    class Config:
        orm_mode = True