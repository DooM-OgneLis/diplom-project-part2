import requests
import allure
from API.base_function import BaseFunction
from data import API

class CreateUser(BaseFunction):
    @allure.step('Отправка формы POST на регистрацию нового пользователя')
    def post_registration_user(self, email = False, password = False, name = False):
        register_form = {}
        if email:
            register_form["email"] = email
        if password:
            register_form["password"] = password
        if name:
            register_form["name"] = name

        request = requests.post(
                            API.CREATE_USER,
                            json=register_form
                        )
        return request