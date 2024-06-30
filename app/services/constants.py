from app.core.config import settings

DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'

LOCALE = 'ru_RU'

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

ROW_COUNT = 100
COLUMN_COUNT = 5

SPREADSHEET_BODY = {
    'properties': {
        'title': 'Отчёт',
        'locale': LOCALE
    },
    'sheets': [
        {'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Отчет по проинвестированным проектам',
            'gridProperties': {
                'rowCount': ROW_COUNT,
                'columnCount': COLUMN_COUNT
            }
        }}
    ]
}

TABLE_VALUES = [
    ['Отчёт'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
