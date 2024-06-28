from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class ProjectDonationModel(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_check'),
        CheckConstraint(
            'full_amount >= invested_amount',
            name='full_more_than_invested'
        )
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    close_date = Column(DateTime)

    class Config:
        min_anystr_length = 1
