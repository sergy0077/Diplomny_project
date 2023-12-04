from tortoise import Tortoise, fields
from tortoise.models import Model


class YourModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)


TORTOISE_ORM = {
    "connections": {
        "default": "postgres://sergy007:11223344@localhost:5432/diplom",
    },
    "apps": {
        "models": {
            "models": ["app.app_models", "app.auth.auth_models",  "aerich.models"],
            "default_connection": "default",
        }
    }
}


async def init():
    # await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.init(
        config=TORTOISE_ORM,
        models={'models': ["app.app_models", "app.auth.auth_models", "aerich.models"]}
    )
    await Tortoise.generate_schemas()


async def close():
    await Tortoise.close_connections()