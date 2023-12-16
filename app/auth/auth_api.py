from fastapi import FastAPI, APIRouter
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from starlette.requests import Request
from settings import settings
from app.app_api import api_router as api_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

auth_app = FastAPI(default_response_class=JSONResponse)
auth_router = APIRouter()

'''
Определяет APIRouter для авторизации, регистрирует маршруты из других модулей и обработчики событий.
'''

@auth_app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "msg": "Validation error"},
    )

# Include routes from other modules
auth_router.include_router(api_router)


class TortoiseSettings:
    db_url = settings.database_url
    modules = {"models": ["app.auth.auth_models", "app.app_models"]}


# Register Tortoise with FastAPI
register_tortoise(
    auth_app,
    config=TortoiseSettings,
    generate_schemas=True,
    add_exception_handlers=True,
)


# Event handlers
@auth_app.on_event("startup")
async def startup_event():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["app.app_models", "app.app_models"]})

    await Tortoise.generate_schemas()


@auth_app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()


@auth_app.exception_handler(DoesNotExist)
async def does_not_exist_exception_handler(request: Request, exc: DoesNotExist):
    return JSONResponse(status_code=404, content={"message": "Object not found"})

