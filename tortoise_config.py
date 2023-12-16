TORTOISE_ORM = {
    "connections": {
        "default": "postgres://sergy007:130468@localhost:5432/diplom",
    },
    "apps": {
        "models": {
            "models": [
                "app.app_models",
                "app.auth.auth_models",
                "aerich.models"
            ],
            "default_connection": "default",
        }
    }
}