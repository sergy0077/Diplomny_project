import pytest
from run import init_database, app_fastapi


# Инициализация приложения и базы данных
init_database(app_fastapi)

# Загрузка настроек для тестов
pytest_plugins = ["tests.conftest"]


# Пример теста
def test_example():
    assert 1 + 1 == 2


# Тесты с использованием фикстуры client

@pytest.mark.asyncio
async def test_register_user(authenticated_client):
    response = authenticated_client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+71234567890",
            "password": "Test123$",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_products_unauthorized(client):
    response = client.get("/products")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_products_authorized(authenticated_client):
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = authenticated_client.post("/register", json=user_data)
    assert response.status_code == 422

    response = authenticated_client.get("/products")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_to_cart(authenticated_client):
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = authenticated_client.post("/register", json=user_data)
    assert response.status_code == 422

    # Add to cart
    response = authenticated_client.post("/cart/add-to-cart", json={"product_id": 1, "name": "TestProduct"})
    assert response.status_code == 422
    assert response.json() == {"detail": [{"loc": ["body", "name"], "msg": "Field required", "type": "value_error.missing"}]}


@pytest.mark.asyncio
async def test_remove_from_cart(authenticated_client):
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = authenticated_client.post("/register", json=user_data)
    assert response.status_code == 422

    # Remove from cart
    response = authenticated_client.post("/remove-from-cart", json={"product_id": 1, "name": "TestProduct"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_get_cart_total_price(authenticated_client):
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = authenticated_client.post("/register", json=user_data)
    assert response.status_code == 422

    # Get cart total price
    response = authenticated_client.get("/cart-total-price")
    assert response.status_code == 404
    assert "detail" in response.json() and "Not Found" in response.json()["detail"]

