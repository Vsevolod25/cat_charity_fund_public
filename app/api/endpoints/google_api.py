from http import HTTPStatus

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charityproject_crud
from app.services import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)
router = APIRouter()


@router.post(
    '/',
    response_model=dict[str, str],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

) -> dict[str, str]:
    """Создание отчета о закрытых проектах."""
    time_projects = await charityproject_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(
        wrapper_services
    )
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id, time_projects, wrapper_services
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=error.args[0]
        )
    return {'URL': spreadsheet_url}
