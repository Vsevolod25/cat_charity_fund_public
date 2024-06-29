from datetime import datetime
from typing import Tuple, Union

from aiogoogle import Aiogoogle

from app.models import CharityProject
from .constants import (
    BASE_TABLE_VALUES,
    COLUMN_COUNT,
    DATETIME_FORMAT,
    LOCALE,
    PERMISSIONS_BODY,
    ROW_COUNT,
    SHEETS
)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> Tuple[str]:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт от {now_date_time}',
            'locale': LOCALE
        },
        'sheets': SHEETS
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        time_projects: list[Tuple[int, CharityProject]],
        wrapper_services: Aiogoogle
) -> Union[None, ValueError]:
    now_date_time = datetime.now().strftime(DATETIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        *BASE_TABLE_VALUES
    ]
    if time_projects:
        for project in time_projects:
            table_values.append(
                [project[1].name, project[0], project[1].description]
            )
    else:
        table_values.append(['Нет информации о закрытых проектах'])

    if (len(table_values) > ROW_COUNT) or (COLUMN_COUNT < 3):
        raise ValueError(
            'Таблица недостаточного размера для отображения проектов.'
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
