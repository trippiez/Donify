from pydantic import BaseModel, Field, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100
    )
    description: str = Field(
        ..., min_length=1
    )
    full_amount: PositiveInt = Field(...)


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int

    class Config:
        orm_mode = True