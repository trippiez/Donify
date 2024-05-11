from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AbstractBaseSchema(BaseModel):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True