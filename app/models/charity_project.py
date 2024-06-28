from sqlalchemy import Column, String, Text

from .base import ProjectDonationModel


class CharityProject(ProjectDonationModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
