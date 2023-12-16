from fastapi import FastAPI

from app.app_main import app as app_fastapi

# app_fastapi = app


def init_database(application: FastAPI) -> None:
    from tortoise.contrib.fastapi import register_tortoise
    register_tortoise(
        application,
        db_url="postgres://postgres:130468@localhost:5432/diplom",
        modules={"models": ["app.app_models", "app.auth.auth_models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


if __name__ == '__main__':
    import uvicorn

    init_database(app_fastapi)
    uvicorn.run("run:app_fastapi")
