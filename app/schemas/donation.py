from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    comment: Optional[str]
    full_amount: Annotated[int, Field(strict=True, gt=0)]

    class Config:
        extra = Extra.forbid


class DonationShortDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationShortDB):
    user_id: int
    invested_amount: int = Field(default=0, strict=True, ge=0)
    fully_invested: bool = Field(default=False)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
