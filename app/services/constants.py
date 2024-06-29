from app.core.config import settings

BASE_TABLE_VALUES = [
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

LOCALE = 'ru_RU'

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

ROW_COUNT = 100
COLUMN_COUNT = 5

SHEETS = [
    {
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Отчет по проинвестированным проектам',
            'gridProperties': {
                'rowCount': ROW_COUNT, 'columnCount': COLUMN_COUNT
            }
        }
    }
]
