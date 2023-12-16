from fastapi import APIRouter, Depends, HTTPException,  Form
from fastapi.security import OAuth2PasswordRequestForm
from app.app_services import create_user, get_products, create_product
from app.auth.auth_services import authenticate_user, create_access_token
from app.app_models import User, Product, ProductInDB, ProductCreate
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List


api_router = APIRouter(default_response_class=JSONResponse)


class RegisterUser(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str


@api_router.post("/register")
async def register_user_endpoint(user_data: RegisterUser):
    user = await create_user(user_data.full_name, user_data.email, user_data.phone, user_data.password)
    return {"message": "User registered successfully", "user": user}


@api_router.post("/token")
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Неправильный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.get("/users/me")
async def read_users_me(current_user: User = Depends(authenticate_user)):
    return current_user


class CreateProduct(BaseModel):
    name: str
    price: float


class ProductModel(BaseModel):
    name: str
    price: int
    created_at: str
    updated_at: str
    is_active: bool


@api_router.post("/products", response_model=ProductInDB)
async def create_product_endpoint(product_data: ProductCreate):
    product = await create_product(name=product_data.name, price=product_data.price)
    return ProductInDB(**product.dict())


@api_router.get("/products", response_model=List[ProductInDB])
async def get_products_endpoint(page: int = 1, page_size: int = 10):
    products = await get_products(page, page_size)
    return products

