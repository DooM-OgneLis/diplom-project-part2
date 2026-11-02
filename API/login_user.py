import requests
import allure
from API.base_function import BaseFunction
from data import API

class LoginUser(BaseFunction):
    @allure.step('Отправка формы POST на авторизацию пользователя')
    def post_autorization_user(self, email, password):
        login_form = {}

        if email:
            login_form["email"] = email
        if password:
            login_form["password"] = password

        request = requests.post(
                            API.AUTHORIZATION,
                            json=login_form
                        )
        return request