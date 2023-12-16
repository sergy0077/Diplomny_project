from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str
    tortoise_orm: str

    class Config:
        env_file = ".env"


settings = Settings()


SECRET_KEY = 'django-insecure-!mo#k*0%926(1h70y^xs!r8w48vj&m*o^%3rgi6m)1xoj(7e1j'
