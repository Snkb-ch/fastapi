from fastapi.testclient import TestClient
from main import app  # Импортируйте ваше приложение FastAPI

client = TestClient(app)
import pytest
from httpx import AsyncClient
from main import app


# get token for testing /login

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def token(client):
    # Подготовка тестового пользователя
    test_user = {"username": "user@example.com", "password": "123"}


    # Получение токена
    response = client.post("/login", data=test_user)
    return response.json()["access_token"]


def test_read_books(client, token):
    response = client.get("/books/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_book(client, token):
    response = client.post("/books/", json={"title": "test book", "author": "test author", "year_of_publication": 2021, "category": "test category"}, headers = {"Authorization": f"Bearer {token}"})

    assert response.status_code == 201

    book_id = response.json()["id"]
    response = client.get(f"/books/{book_id}", headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.put(f"/books/{book_id}", json={"title": "test book 2", "author": "test author", "year_of_publication": 2021, "category": "test category"}, headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.get("/books/search?title=test book 2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200




    response = client.post(f"/books/rent/{book_id}", headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response = client.post(f"/books/return/{book_id}", headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    response = client.post(f"/books/{book_id}/favorite", headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    response = client.get(f"/books/search?favorite=true", headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 200







    response = client.delete(f"/books/{book_id}", headers = {"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
