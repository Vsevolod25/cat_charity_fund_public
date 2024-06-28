# QRKot

## Описание
API приложения для сбора средств на благотворительные проекты по помощи котам.
Администраторы размещают информацию о доступных проектах и целях сбора.
Пользователи могут присылать пожертвования для достижения этих целей.
Выбор проекта не предусмотрен, средства со всех пожертвованией распределяются последовательно на все доступные проекты в порядке их размещения на платформе.

## Технологии
aiofiles==0.8.0; python_version >= '3.6' and python_version < '4'
aiogoogle==4.2.0
aiohttp==3.8.1; python_version >= '3.6'
aiosignal==1.2.0; python_version >= '3.6'
aiosqlite==0.17.0
alembic==1.7.7
anyio==3.6.1
asgiref==3.5.2
async-timeout==4.0.2; python_version >= '3.6'
attrs==21.4.0
bcrypt==3.2.2
cachetools==5.2.0; python_version ~= '3.7'
certifi==2022.5.18.1
cffi==1.15.0
charset-normalizer==2.0.12
click==8.1.3
cryptography==37.0.2
dnspython==2.2.1
email-validator==1.2.1
faker==12.0.1
fastapi-users-db-sqlalchemy==4.0.3
fastapi-users[sqlalchemy]==10.0.4
fastapi==0.78.0
flake8==4.0.1
freezegun==1.2.1
frozenlist==1.3.0; python_version >= '3.7'
google-auth==2.8.0
greenlet==1.1.2
h11==0.13.0
httptools==0.4.0
idna==3.3
iniconfig==1.1.1
lock==2018.3.25.2110
makefun==1.13.1
mako==1.2.0
markupsafe==2.1.1
mccabe==0.6.1
mixer==7.2.2
multidict==6.0.2; python_version >= '3.7'
packaging==21.3; python_version >= '3.6'
passlib[bcrypt]==1.7.4
pluggy==1.0.0
py==1.11.0
pyasn1-modules==0.2.8
pyasn1==0.4.8
pycodestyle==2.8.0
pycparser==2.21
pydantic==1.9.1
pyflakes==2.4.0
pyjwt[crypto]==2.3.0
pyparsing==3.0.9
pytest-asyncio==0.23.4
pytest-freezegun==0.4.2
pytest-lazy-fixture==0.6.3
pytest-pythonpath==0.7.3
pytest==7.1.3
python-dateutil==2.8.2
python-dotenv==0.20.0
python-multipart==0.0.5
pyyaml==6.0
requests==2.27.1
rsa==4.8; python_version >= '3.6'
six==1.16.0
sniffio==1.2.0
sqlalchemy==1.4.36
starlette==0.19.1
toml==0.10.2
tonyg-rfc3339==0.1
typing-extensions==4.2.0
urllib3==1.26.9
uvicorn[standard]==0.17.6
uvloop==0.16.0
watchgod==0.8.2
websockets==10.3
yarl==1.7.2; python_version >= '3.6'

## Как использовать

Запуск производится из консоли. При первом запуске выполните следующие команды:

```
cd cat_charity_fund
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app
```

В дальнейшем (при отсутствии изменений в проекте) достаточно ввести последнюю команду:

```
uvicorn app.main:app
```

После этого программа будет запущена на локальном устройстве: http://127.0.0.1:8000

Документация со всеми возможными запросами доступна по ссылке: http://127.0.0.1:8000/docs

Любой пользователь может запросить список проектов и создать аккаунт.
Зарегистрированные пользователи могут отправлять пожертвования и запрашивать информацию об уже отправленных.
Добавление, редактирование, удаление проектов и информация о всех совершенных пожертвованиях доступна только суперпользователю.

При первом запуске программы на локальном устройстве может быть создан аккаунт суперпользователя. Для этого необходимо указать FIRST_SUPERUSER_EMAIL и FIRST_SUPERUSER_PASSWORD в локальном .env или в настройках
```
cat_charity_fund/app/core/config.py
```

Информация о проектах и пожертвованиях сохраняется в базе данных
```
cat_charity_fund/fastapi.db
```

## Автор

Vsevolod25: https://github.com/Vsevolod25