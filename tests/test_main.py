import pytest
from fastapi.testclient import TestClient
from app.app_main import app
from app.app_models import User
from app.cart import Product

client = TestClient(app)


@pytest.mark.asyncio
async def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "john@example.com",
            "phone": "+71234567890",
            "password": "Test123$",
        },
    )
    assert response.status_code == 201
    # assert response.json()["user_id"] is not None


@pytest.mark.asyncio
async def test_get_products_unauthorized():
    response = client.get("/products")
    assert response.status_code == 401
    # assert response.json()["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_get_products_authorized():
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    response = client.post("/auth/token", data={"username": "john@example.com", "password": "Test123$"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/products", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 0


@pytest.mark.asyncio
async def test_add_to_cart():
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Get user token
    response = client.post("/token", data={"username": "john@example.com", "password": "Test123$"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Add a product to the cart
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/add-to-cart/SomeProduct", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "SomeProduct добавлен в корзину"


@pytest.mark.asyncio
async def test_remove_from_cart():
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Get user token
    response = client.post("/token", data={"username": "john@example.com", "password": "Test123$"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Remove a product from the cart
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/remove-from-cart/SomeProduct", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "SomeProduct удален из корзины"


@pytest.mark.asyncio
async def test_get_cart_total_price():
    # Assuming the user is already registered
    user_data = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+71234567890",
        "password": "Test123$",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Get user token
    response = client.post("/token", data={"username": "john@example.com", "password": "Test123$"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Get total price of the cart
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/cart-total-price", headers=headers)
    assert response.status_code == 200
    assert "total_price" in response.json()