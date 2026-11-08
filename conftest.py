import pytest
import generator
from API.create_user import CreateUser
import API.delete_user as du

@pytest.fixture(scope="function")
def registration_user():
    new_user = CreateUser()
    email = generator.email_generator()
    password = generator.password_generator()
    name = generator.name_generator()

    reqest = new_user.post_registration_user(email, password, name)

    return {
        'email': email,
        'password': password,
        'name': name,
        'accessToken': reqest.json()['accessToken'],
        'refreshToken': reqest.json()['refreshToken']
    }

@pytest.fixture(scope="function")
def delete_user():
    container = {}

    yield container

    token = container.get("accessToken")
    if token:
        try:
            du.delete_user(token)
        except Exception as e:
            print(f"[Cleanup] Ошибка удаления: {e}")