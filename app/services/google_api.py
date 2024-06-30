from datetime import datetime
from http import HTTPStatus
from typing import Tuple, Union

from aiogoogle import Aiogoogle
from fastapi import HTTPException

from app.models import CharityProject
from .constants import (
    BASE_TABLE_VALUES,
    COLUMN_COUNT,
    DATETIME_FORMAT,
    PERMISSIONS_BODY,
    ROW_COUNT,
    SPREADSHEET_BODY
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> Tuple[str]:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEET_BODY
    spreadsheet_body['properties']['title'] = now_date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        time_projects: list[Tuple[int, CharityProject]],
        wrapper_services: Aiogoogle
) -> Union[None, ValueError]:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = BASE_TABLE_VALUES
    table_values[0] = ['Отчёт от', now_date_time]
    if time_projects:
        for project in time_projects:
            table_values.append(
                [project[1].name, project[0], project[1].description]
            )
    else:
        table_values.append(['Нет информации о закрытых проектах'])

    if len(table_values) > ROW_COUNT or COLUMN_COUNT < len(table_values[-1]):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                'Таблица недостаточного размера для отображения проектов. '
                f'Таблица: {ROW_COUNT} строк, {COLUMN_COUNT} столбцов. '
                f'Полученные данные: {len(table_values)} строк, '
                f'{len(table_values[-1])} столбцов'
            )
        )

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'1:{ROW_COUNT}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
