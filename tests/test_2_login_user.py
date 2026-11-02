import allure
import pytest
import API.login_user as LU
from data import API, Request, IgnoreList

class TestLoginUser:

    @allure.title("Проверка авторизации пользователя")
    def test_autorization_user_login_user(self, registration_data):
        action = LU.LoginUser()

        #формирования предданных для проверки
        status_code = 200 #не задан в документации API, по умолчанию код 200 для авторизации
        message_check = Request.AUTHORIZATION['success']
        message_check["user"]["email"] = registration_data['email']
        message_check["user"]["name"] = registration_data['name']

        allure.dynamic.description(
            f"Отправить запрос POST на авторизацию пользователя.\n"
            f"Действие: отправка POST с данными: {registration_data['email']}, {registration_data['password']} на {API.AUTHORIZATION}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_autorization_user(registration_data['email'], registration_data['password'])
        
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check, IgnoreList.TOKEN) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')
        #проверка сохранности токенов при авторизации
        assert action.check_tokens(reqest.json(), registration_data, True) == 'Ok', ('Токе не изменился, проверь сообщение ошибки')

        #обновляем токены после авторизации и проверки
        registration_data['accessToken'] = reqest.json()['accessToken']
        registration_data['refreshToken'] = reqest.json()['refreshToken']
        
    
    @allure.title("Проверка авторизации пользователя с неверными данными")
    @pytest.mark.parametrize(
        'email, password', 
        [[False, 'qwerty1234'],['vasya@avtomat.ru',False],['vasya@avtomat.ru','qwerty1234']],
        ids=["no_email", "no_password", "uncorrect_write"]
        )
    def test_autorization_user_uncorrect_write_user(self, email, password):
        action = LU.LoginUser()

        #формирования предданных для проверки
        status_code = 401
        message_check = Request.AUTHORIZATION['denite']

        allure.dynamic.description(
            f"Отправить запрос POST на авторизацию пользователя.\n"
            f"Действие: отправка POST с данными: {email}, {password} на {API.AUTHORIZATION}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_autorization_user(email, password)
        
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

    @allure.title("Проверка авторизации пользователя с неверным паролем")
    def test_autorization_user_uncorrect_write_user_password(self, registration_data):
        action = LU.LoginUser()

        #формирования предданных для проверки
        status_code = 401 
        message_check = Request.AUTHORIZATION['denite']
        password = 'qwerty1234'

        allure.dynamic.description(
            f"Отправить запрос POST на авторизацию пользователя.\n"
            f"Действие: отправка POST с данными: {registration_data['email']}, {password} на {API.AUTHORIZATION}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_autorization_user(registration_data['email'], password)
        
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

