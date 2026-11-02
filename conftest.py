import pytest
import generator

@pytest.fixture(scope="session")
def registration_data():
    email = generator.email_generator()
    password = generator.password_generator()
    firstName = generator.name_generator()
    return {
        'email': email,
        'password': password,
        'name': firstName
    }