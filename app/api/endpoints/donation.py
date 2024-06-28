from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charityproject_crud, donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationShortDB
from app.services import invest_donations

router = APIRouter()


@router.post('/', response_model=DonationShortDB)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание пожертвования. Для зарегистрированных пользователей."""
    donation_data = donation.dict()
    open_projects = await charityproject_crud.get_not_fully_invested(session)
    if open_projects:
        donation_data, invested = invest_donations(
            instance=donation_data, funds=open_projects
        )
        for obj in invested:
            session.add(obj)
    return await donation_crud.create(donation_data, session, user)


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Список пожертвований. Для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationShortDB])
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Список пожертвований пользователя.
    Для зарегистрированных пользователей.
    """
    return await donation_crud.get_donations_by_user(user.id, session)
