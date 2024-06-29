from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import Donation


class CRUDDonation(CRUDBase):

    async def get_donations_by_user(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> list[Donation]:
        """Получение списка пожертвований пользователя."""
        attr = getattr(self.model, 'user_id')
        db_obj = await session.execute(
            select(Donation).where(attr == user_id)
        )
        return db_obj.scalars().all()


donation_crud = CRUDDonation(Donation)
