import allure
import pytest
import API.create_user as CU
from data import API, Request, IgnoreList

class TestRegistrationUser:

    @allure.title("Проверка создания нового пользователя")
    def test_registration_user_new_user(self, registration_data):
        action = CU.CreateUser()
        
        #формирования предданных для проверки
        status_code = 201 #не задан в документации API, по умолчанию код 201 для регистрации
        message_check = Request.CREATE_USER['Created']
        message_check["user"]["email"] = registration_data['email']
        message_check["user"]["name"] = registration_data['name']

        allure.dynamic.description(
            f"Отправить запрос POST на регистрацию нового пользователя.\n"
            f"Действие: отправка POST с данными: {registration_data} на {API.CREATE_USER}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_registration_user(registration_data['email'], registration_data['password'], registration_data['name'])

        registration_data['accessToken'] = reqest.json()['accessToken']
        registration_data['refreshToken'] = reqest.json()['refreshToken']
        
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check, IgnoreList.TOKEN) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

    @allure.title("Проверка создания пользователя который уже существует в базе (дублирующий)")
    def test_registration_user_double_user(self, registration_data):
        action = CU.CreateUser()

        #формирования предданных для проверки
        status_code = 403
        message_check = Request.CREATE_USER['double']

        allure.dynamic.description(
            f"Отправить запрос POST на регистрацию нового пользователя.\n"
            f"Действие: отправка POST с данными: {registration_data} на {API.CREATE_USER}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_registration_user(registration_data['email'], registration_data['password'], registration_data['name'])

        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

    @allure.title("Проверка создания пользователя без обязательного поля")
    @pytest.mark.parametrize(
        'key', 
        ['email', 'password', 'name'], 
        ids=["no_email", "no_password", "no_name"]
        )
    def test_registration_user_mandatory_user_field(self, registration_data, key):
        action = CU.CreateUser()

        #формирования предданных для проверки
        status_code = 403
        message_check = Request.CREATE_USER['mandatory']
        reg_data = registration_data.copy()
        reg_data[key] = False

        allure.dynamic.description(
            f"Отправить запрос POST на регистрацию нового пользователя.\n"
            f"Действие: отправка POST с данными: {reg_data} на {API.CREATE_USER}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_registration_user(reg_data['email'], reg_data['password'], reg_data['name'])

        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')
