from tortoise import Tortoise
from fastapi import FastAPI
from .app_main import app, settings

Tortoise.init(
    db_url=settings.tortoise_orm,
    modules={'models': ['app.app_models']},
)


@app.on_event("startup")
async def startup_db_client():
    await Tortoise.generate_schemas()


@app.on_event("shutdown")
async def shutdown_db_client():
    await Tortoise.close_connections()





# from tortoise import Tortoise
# from tortoise.contrib.fastapi import register_tortoise
# from fastapi import FastAPI
# from app.app_main import settings
# from .app_main import app
#
# app = FastAPI()
#
# '''
# инициализирует приложение и Tortoise ORM.
# Загружает модели из app.models.
# Регистрирует маршруты из app.app_api.
# '''
#
# # Set up Tortoise ORM
# Tortoise.init_models(["app.app_models"], "models")
# Tortoise.init(config=settings.tortoise_orm)
#
# # Register Tortoise with FastAPI
# register_tortoise(
#     app,
#     db_url='sqlite://db.sqlite3',
#     modules={'models': ['app.models']},
#     generate_schemas=True,
#     add_exception_handlers=True
# )
#
#
# from app import app_api






# from tortoise import Tortoise
# from fastapi import FastAPI
# from .app_main import app
# from .app_main import settings
#
# Tortoise.init(
#     db_url=settings.tortoise_orm,
#     models={"app.app_models": ["app.app_models"]},
# )
#
# @app.on_event("startup")
# async def startup_db_client():
#     await Tortoise.generate_schemas()
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     await Tortoise.close_connections()
