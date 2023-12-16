from tortoise.models import Model
from tortoise import fields
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=15, unique=True)
    password_hash = fields.CharField(max_length=255)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, plain_password):
        self.password_hash = pwd_context.hash(plain_password)

    def verify_password(self, plain_password):
        try:
            return pwd_context.verify(plain_password, self.password_hash)
        except pwd_context.exc.UnknownHashError:
            # Если возникает UnknownHashError, обновим хэш пароля
            if pwd_context.needs_update(self.self.password_hash, "bcrypt"):
                new_hash = pwd_context.hash(plain_password)
                self.password_hash = new_hash
                self.save()
                return True
            return False

    def create_user(self, full_name: str, email: str, phone: str, password: str):
        hashed_password = pwd_context.hash(password)
        # Сохранение hashed_password в базе данных
        user = self.create(full_name=full_name, email=email, phone=phone, password_hash=hashed_password)
        return user


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    price = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    is_active = fields.BooleanField(default=True)


class ProductBase(BaseModel):
    name: str
    price: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = True


class ProductCreate(ProductBase):
    additional_field: str


class ProductInDB(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class ProductOut(ProductInDB):
    additional_field: str
