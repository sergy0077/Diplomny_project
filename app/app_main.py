from fastapi import FastAPI
from app.app_api import api_router
from app.cart_routes import router as cart_router
from app.auth.auth_api import auth_router
from fastapi.openapi.models import OpenAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.responses import HTMLResponse
from fastapi import Request


app = FastAPI()


# Общая информация об API
app.title = "My Awesome API"
app.version = "1.0.0"
app.description = "This is an awesome API for my project."


# Дополнительные метаданные
app.openapi = {
    "info": {
        "title": "My API",
        "version": "1.0.0",
        "description": "This is my API",
        "terms_of_service": "http://example.com/terms/",
        "contact": {
            "name": "API Support",
            "url": "http://www.example.com/support/",
            "email": "support@example.com",
        },
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
        },
    }
}

def custom_swagger_ui_html(*, request: Request) -> HTMLResponse:
    openapi_url = app.openapi_url
    swagger_ui = get_swagger_ui_html(
        openapi_url=openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=app.swagger_ui_swagger_js_url,
        swagger_css_url=app.swagger_ui_swagger_css_url,
    )
    return HTMLResponse(content=swagger_ui)

def custom_redoc_html(*, request: Request) -> HTMLResponse:
    openapi_url = app.openapi_url
    redoc_ui = get_redoc_html(
        openapi_url=openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url=app.redoc_js_url,
        redoc_css_url=app.redoc_css_url,
    )
    return HTMLResponse(content=redoc_ui)


@app.get("/")
def read_root():
    return {"message": "Hello, world!"}


# Register API and Auth routers
app.include_router(api_router)
app.include_router(cart_router, prefix="/cart", tags=["cart"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Добавляем Swagger UI
app.add_route("/docs", custom_swagger_ui_html, name="swagger_ui")

# Добавляем ReDoc
app.add_route("/redoc", custom_redoc_html, name="redoc")


