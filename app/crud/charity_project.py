from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_projects_by_name(
            self,
            name: str,
            session: AsyncSession
    ) -> list[CharityProject]:
        """Получение проекта по названию."""
        attr = getattr(self.model, 'name')
        db_obj = await session.execute(
            select(CharityProject).where(attr == name)
        )
        return db_obj.scalars().all()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[CharityProject]:
        """
        Получение всех закрытых проектов
        и сортировка по скорости завершения сбора.
        """
        attr = getattr(self.model, 'fully_invested')
        charityprojects = await session.execute(
            select(self.model).where(attr == 1)
        )
        charityprojects = charityprojects.scalars().all()
        time_projects = []
        for project in charityprojects:
            time = project.close_date - project.create_date
            time_projects.append((str(time), project))
        return sorted(time_projects)


charityproject_crud = CRUDCharityProject(CharityProject)
