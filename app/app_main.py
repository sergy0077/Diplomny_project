from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from settings import settings
from app.app_api import api_router
from app.cart_routes import router as cart_router

app = FastAPI()

'''
Инициализирует FastAPI.
Регистрирует маршруты из app.app_api и app.auth.auth_api.
Задает обработчики событий startup и shutdown для Tortoise.
'''

# Register API and Auth routers
app.include_router(api_router)
app.include_router(cart_router, prefix="/cart", tags=["cart"])


class TortoiseSettings:
    db_url = settings.database_url
    modules = {"models": ["app.app_models"]}


register_tortoise(
    app,
    config=TortoiseSettings,
    generate_schemas=True,
    add_exception_handlers=True,
)


# Event handlers
@app.on_event("startup")
async def startup_event():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.app_models"]},
    )
    await Tortoise.generate_schemas()


@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()









# @app.on_event("startup")
# async def startup_event():
#     await Tortoise.init(config=TortoiseSettings)
#     await Tortoise.generate_schemas()


# register_tortoise(
#     app,
#     db_url=settings.database_url,
#     modules={"models": ["app.models"]},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )
#
#
# # Event handlers
# @app.on_event("startup")
# async def startup_event():
#     await Tortoise.init(
#         db_url=settings.database_url,
#         modules={"models": ["app.models"]},
#     )
#     await Tortoise.generate_schemas()


