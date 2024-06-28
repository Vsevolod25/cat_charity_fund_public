from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount,
    check_fully_invested,
    check_investments_exist,
    check_project_exists,
    check_unique_name
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charityproject_crud, donation_crud
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services import invest_donations

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создание проекта. Для суперюзеров."""
    await check_unique_name(charityproject.name, session)
    charityproject_data = charityproject.dict()
    open_donations = await donation_crud.get_not_fully_invested(session)
    if open_donations:
        charityproject_data, invested = invest_donations(
            instance=charityproject_data, funds=open_donations
        )
        for obj in invested:
            session.add(obj)
    return await charityproject_crud.create(charityproject_data, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_charityproject(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Изменение проекта. Для суперюзеров."""
    charityproject = await check_project_exists(project_id, session)
    check_fully_invested(charityproject)
    if obj_in.name:
        await check_unique_name(obj_in.name, session, project_id)
    if obj_in.full_amount is not None:
        check_full_amount(
            new_full_amount=obj_in.full_amount,
            charityproject=charityproject
        )
        if obj_in.full_amount == charityproject.invested_amount:
            charityproject.fully_invested = True
            charityproject.close_date = datetime.now()
    return await charityproject_crud.update(
        db_obj=charityproject,
        obj_in=obj_in,
        session=session,
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charityproject(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление проекта. Для суперюзеров."""
    charityproject = await check_project_exists(project_id, session)
    check_investments_exist(charityproject)
    return await charityproject_crud.remove(charityproject, session)


@router.get('/', response_model=list[CharityProjectDB])
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session)
):
    """Список всех проектов."""
    return await charityproject_crud.get_multi(session)
