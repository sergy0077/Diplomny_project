from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth_services import authenticate_user, create_access_token
from app.app_models import User
from fastapi.responses import JSONResponse


api_router = APIRouter(default_response_class=JSONResponse)

# api_router = APIRouter()

'''
определяет APIRouter и включает маршруты из других модулей
'''


@api_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.get("/users/me")
async def read_users_me(current_user: User = Depends(authenticate_user)):
    return current_user
