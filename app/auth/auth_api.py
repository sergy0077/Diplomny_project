from fastapi import FastAPI, APIRouter, Depends, HTTPException
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from starlette.responses import JSONResponse

from settings import settings
from app.app_api import api_router as api_router
from fastapi.responses import JSONResponse

from fastapi.exceptions import RequestValidationError


# auth_router = FastAPI()
# auth_router = APIRouter(default_response_class=JSONResponse)
auth_app = FastAPI(default_response_class=JSONResponse)
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
auth_app.include_router(api_router)


class TortoiseSettings:
    db_url = settings.database_url
    modules = {"models": ["app.auth.auth_models"]}


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
        modules={"models": ["app.app_models"]})

    await Tortoise.generate_schemas()


@auth_app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()


@auth_app.exception_handler(DoesNotExist)
async def does_not_exist_exception_handler(request: Request, exc: DoesNotExist):
    return JSONResponse(status_code=404, content={"message": "Object not found"})



# from fastapi import Depends, HTTPException, APIRouter
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from tortoise.contrib.fastapi import HTTPNotFoundError
# from app.app_main import app
# from app.auth.auth_services import authenticate_user, create_access_token, get_current_user
# from app.app_models import User
#
# router = APIRouter()
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# @router.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=401,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = await create_access_token(data={"sub": user.email, "scopes": []})
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @router.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

