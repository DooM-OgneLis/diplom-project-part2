import allure
import pytest
import API.create_user as CU
from data import API, Request, IgnoreList
import common

class TestRegistrationUser:

    @allure.title("Проверка создания нового пользователя")
    def test_registration_user_new_user(self, delete_user):
        action = CU.CreateUser()
        
        #формирования предданных для проверки
        registration_data = common.gen_list_register()
        status_code = Request.STATUS_CODE['Created'] #не задан в документации API, по умолчанию код 201 для регистрации
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

        delete_user['accessToken'] = reqest.json()['accessToken']
    
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check, IgnoreList.TOKEN) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

    @allure.title("Проверка создания пользователя который уже существует в базе (дублирующий)")
    def test_registration_user_double_user(self, delete_user):
        action = CU.CreateUser()

        #формирования предданных для проверки
        registration_data = common.gen_list_register()
        status_code = Request.STATUS_CODE['Forbidden']
        message_check = Request.CREATE_USER['double']

        allure.dynamic.description(
            f"Отправить запрос POST на регистрацию нового пользователя.\n"
            f"Действие: отправка POST с данными: {registration_data} на {API.CREATE_USER}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса дважды
        delete_user['accessToken'] = action.post_registration_user(registration_data['email'], registration_data['password'], registration_data['name']).json()['accessToken']
        reqest = action.post_registration_user(registration_data['email'], registration_data['password'], registration_data['name'])

        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

    @allure.title("Проверка создания пользователя без обязательного поля")
    @pytest.mark.parametrize(
        'key', 
        ['email', 'password', 'name'], 
        ids=["no_email", "no_password", "no_name"]
        )
    def test_registration_user_mandatory_user_field(self, key):
        action = CU.CreateUser()

        #формирования предданных для проверки
        registration_data = common.gen_list_register()
        status_code = Request.STATUS_CODE['Forbidden']
        message_check = Request.CREATE_USER['mandatory']
        registration_data[key] = False

        allure.dynamic.description(
            f"Отправить запрос POST на регистрацию нового пользователя.\n"
            f"Действие: отправка POST с данными: {registration_data} на {API.CREATE_USER}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_registration_user(registration_data['email'], registration_data['password'], registration_data['name'])

        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')
