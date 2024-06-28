from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import ProjectDonationModel


class Donation(ProjectDonationModel):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
