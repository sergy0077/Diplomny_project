import asyncio
from tortoise import Tortoise
from app.app_main import settings


async def init():
    await Tortoise.init(
        db_url=settings.tortoise_orm,
        modules={'models': ['app.app_models']},
    )
    await Tortoise.generate_schemas()


async def main():
    await init()

if __name__ == "__main__":
    asyncio.run(init())
