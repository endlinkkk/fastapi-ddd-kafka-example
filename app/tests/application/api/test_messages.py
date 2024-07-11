from fastapi import status
from httpx import Response
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_create_chat_success(app: FastAPI, client: TestClient, faker: Faker):
    url = app.url_path_for("create_chat_handler")
    fake_title = faker.text(max_nb_chars=10)
    response: Response = client.post(url=url, json={"title": fake_title})
    assert response.is_success
    json_data = response.json()

    assert json_data["title"] == fake_title


def test_create_chat_fail_too_long(app: FastAPI, client: TestClient, faker: Faker):
    url = app.url_path_for("create_chat_handler")
    fake_title = faker.text(max_nb_chars=500)
    response: Response = client.post(url=url, json={"title": fake_title})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data["detail"]["error"]


def test_create_chat_fail_too_text_empty(
    app: FastAPI, client: TestClient, faker: Faker
):
    url = app.url_path_for("create_chat_handler")
    response: Response = client.post(url=url, json={"title": ""})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_data = response.json()

    assert json_data["detail"]["error"]
