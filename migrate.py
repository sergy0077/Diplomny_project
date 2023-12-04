from tortoise import Tortoise

Tortoise.init(
    db_url='postgres://diplom',
    modules={'models': ['app.app_models']}
)

Tortoise.generate_schemas()
