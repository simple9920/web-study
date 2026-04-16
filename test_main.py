from fastapi.testclient import TestClient

from main import app
from dependencies import get_current_user
from models import User
import crud

client = TestClient(app)


def override_get_current_user():
    return User(
        id=1,
        email="test@example.com",
        hashed_password="testpassword"
    )


app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_returns_404_for_other_users_item(monkeypatch):
    def fake_get_item(db, item_id, user_id):
        return None
    
    monkeypatch.setattr(crud, "get_item", fake_get_item)

    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_get_item_returns_200_for_own_item(monkeypatch):
    def fake_get_item(db, item_id, user_id):
        return{
            "id": item_id,
            "name": "apple",
            "price": 100,
            "description": "test item",
            "user_id": user_id
        }

    monkeypatch.setattr(crud, "get_item", fake_get_item)

    response = client.get("/items/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "apple"
    assert data["user_id"] == 1

def test_read_items_limit_validation_too_small():
    response = client.get("/items/?limit=0")
    assert response.status_code == 422

def test_read_items_limit_validation_too_large():
    response = client.get("/items/?limit=100")
    assert response.status_code == 422

def test_get_items_requires_authentication():
    app.dependency_overrides = {}

    response = client.get("/items/")

    assert response.status_code == 401

    app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_item_requires_authentication():
    app.dependency_overrides = {}

    response = client.get("/items/1")

    assert response.status_code == 401    

    app.dependency_overrides[get_current_user] = override_get_current_user