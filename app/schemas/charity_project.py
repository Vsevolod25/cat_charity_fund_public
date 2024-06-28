from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProject(BaseModel):
    name: str = Field(max_length=100)
    description: str
    full_amount: int = Field(gt=0)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectUpdate(CharityProject):
    name: Optional[str] = Field(max_length=100)
    description: Optional[str]
    full_amount: Optional[int] = Field(gt=0)


class CharityProjectCreate(CharityProject):
    pass


class CharityProjectDB(CharityProject):
    id: int
    create_date: datetime
    invested_amount: int = Field(default=0, strict=True, ge=0)
    fully_invested: bool = Field(default=False)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
