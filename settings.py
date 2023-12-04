from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    tortoise_orm: str
    # database_url: str = "postgres://sergy007:11223344@localhost/diplom"
    # tortoise_orm: str = "postgres://sergy007:11223344@localhost:3306/diplom"

    class Config:
        env_file = ".env"


settings = Settings()

# from pydantic_settings import BaseSettings
# from typing import Dict, Any
#
#
# class TortoiseORMSettings(BaseSettings):
#     db_url: str
#     modules: Dict[str, Any]
#
#
# class Settings(BaseSettings):
#     database_url: str = "postgres://sergy007:11223344@localhost/diplom"
#     tortoise_orm: TortoiseORMSettings  # Изменено на объект TortoiseORMSettings
#
#     class Config:
#         env_file = ".env"



SECRET_KEY = 'django-insecure-!mo#k*0%926(1h70y^xs!r8w48vj&m*o^%3rgi6m)1xoj(7e1j'