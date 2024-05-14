from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.schemas.base import AbstractBaseSchema
from app.schemas.constants import MAX_NAME_LENGTH, MIN_ANYSTR_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=MAX_NAME_LENGTH)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIN_ANYSTR_LENGTH


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=MAX_NAME_LENGTH)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    class Config:
        min_anystr_length = MIN_ANYSTR_LENGTH


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate, AbstractBaseSchema):
    pass