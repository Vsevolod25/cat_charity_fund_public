from datetime import datetime
from typing import Tuple, Union

from aiogoogle import Aiogoogle

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
    spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
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
    # Переменную table_values нужно объявить,
    # чтобы добавить дату и время отчета, не меняя саму константу
    # (как и в строках 22-23)
    table_values[0] = ['Отчёт от', now_date_time]
    if time_projects:
        for project in time_projects:
            table_values.append(
                [project[1].name, project[0], project[1].description]
            )
    else:
        table_values[1] = ['Нет информации о закрытых проектах']
        table_values.pop(2)

    table_rows = len(table_values)
    table_columns = len(table_values[-1])
    if table_rows > ROW_COUNT or table_columns > COLUMN_COUNT:
        raise ValueError(
            'Таблица недостаточного размера для отображения проектов. '
            f'Таблица: {ROW_COUNT} строк, {COLUMN_COUNT} столбцов. '
            f'Полученные данные: {table_rows} строк, {table_columns} столбцов'
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
