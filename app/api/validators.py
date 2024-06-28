from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charityproject_crud
from app.models import CharityProject


def check_full_amount(
    new_full_amount: int,
    charityproject: CharityProject
) -> CharityProject:
    """
    Проверка новой цели сбора.
    (Не может быть меньше уже внесенных средств).
    """
    if charityproject.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нелья установить значение full_amount '
                'меньше уже вложенной суммы.'
            )
        )


def check_fully_invested(
    charityproject: CharityProject
) -> CharityProject:
    """Проверка статуса проекта."""
    if charityproject.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Закрытый проект нельзя редактировать!'
            )
        )


def check_investments_exist(
    charityproject: CharityProject
) -> str:
    """Проверка внесенных в проект пожертвований перед удалением."""
    if charityproject.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'В проект были внесены средства, не подлежит удалению!'
            )
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка и возврат проекта по id."""
    charityproject = await charityproject_crud.get(project_id, session)
    if not charityproject:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект не найден.'
        )
    return charityproject


async def check_unique_name(
        name: str,
        session: AsyncSession,
        id: Optional[int] = None
) -> str:
    """Проверка уникальности названия проекта."""
    charityproject = await charityproject_crud.get_projects_by_name(
        name, session
    )
    if id:
        charityproject = [
            project for project in charityproject if project.id != id
        ]
    if charityproject:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Проект с таким именем уже существует!'
            )
        )
