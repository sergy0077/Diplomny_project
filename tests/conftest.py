import os
import sys
import asyncio
import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from run import init_database, app_fastapi
from dotenv import load_dotenv


# Инициализация приложения и базы данных
init_database(app_fastapi)

# Загрузка настроек для тестов
load_dotenv('.env.test')


def init_orm():
    register_tortoise(
        app_fastapi,
        db_url='sqlite://:memory:',
        modules={'models': ['app.app_models', 'app.auth.auth_models', 'aerich.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )


# Фикстура создания TestClient после инициализации Tortoise
@pytest.fixture
def client():
    with TestClient(app_fastapi) as c:
        yield c


# Фикстура для event_loop (если используется в ваших тестах)
@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


# Фикстура для authenticated_client
@pytest.fixture
def authenticated_client():
    with TestClient(app_fastapi) as client:
        yield client
