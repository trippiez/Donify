from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.schemas.base import AbstractBaseSchema


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]


class DonationCreate(DonationBase):
    id: int
    create_date: datetime


class DonationDB(DonationBase, AbstractBaseSchema):
    pass