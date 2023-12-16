TORTOISE_TEST_CONFIG = {
    "connections": {
        "default": "postgres://sergy007:130468@localhost:5432/diplom_test",
    },
    "apps": {
        "models": [
            "app.app_models",
            "app.auth.auth_models",
            "aerich.models"
        ],
        "default_connection": "default",
    }
}
