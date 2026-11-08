import allure
import pytest
import API.login_user as LU
from data import API, Request, IgnoreList

class TestLoginUser:

    @allure.title("Проверка авторизации пользователя")
    def test_autorization_user_login_user(self, registration_user, delete_user):
        action = LU.LoginUser()

        #формирования предданных для проверки
        status_code = Request.STATUS_CODE['OK'] #не задан в документации API, по умолчанию код 200 для авторизации
        message_check = Request.AUTHORIZATION['success']
        message_check["user"]["email"] = registration_user['email']
        message_check["user"]["name"] = registration_user['name']
        action.logout(registration_user['refreshToken']) #после регистрации вход производится автоматически, что мешает прохождению теста, производится выход из системы

        allure.dynamic.description(
            f"Отправить запрос POST на авторизацию пользователя.\n"
            f"Действие: отправка POST с данными: {registration_user['email']}, {registration_user['password']} на {API.AUTHORIZATION}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_autorization_user(registration_user['email'], registration_user['password'])

        delete_user['accessToken'] = reqest.json()['accessToken']
        
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check, IgnoreList.TOKEN) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')
        #проверка сохранности токенов при авторизации
        assert action.check_tokens(reqest.json(), registration_user, True) == 'Ok', (f"Токен не изменился, проверь сообщение ошибки:\n{reqest.json()['accessToken']}\n{registration_user['accessToken']}")      
    
    @allure.title("Проверка авторизации пользователя с неверными данными")
    @pytest.mark.parametrize(
        'email, password', 
        [[False, 'qwerty1234'],['vasya@avtomat.ru',False],['vasya@avtomat.ru','qwerty1234']],
        ids=["no_email", "no_password", "uncorrect_write"]
        )
    def test_autorization_user_uncorrect_write_user(self, email, password):
        action = LU.LoginUser()

        #формирования предданных для проверки
        status_code = Request.STATUS_CODE['Unauthorized']
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
    def test_autorization_user_uncorrect_write_user_password(self, registration_user):
        action = LU.LoginUser()

        #формирования предданных для проверки
        status_code = Request.STATUS_CODE['Unauthorized'] 
        message_check = Request.AUTHORIZATION['denite']
        password = 'qwerty1234'

        allure.dynamic.description(
            f"Отправить запрос POST на авторизацию пользователя.\n"
            f"Действие: отправка POST с данными: {registration_user['email']}, {password} на {API.AUTHORIZATION}.\n"
            f"Ожидаемый результат: получен статус код {status_code} с сообщением {message_check}."
        )

        #выполнение запроса
        reqest = action.post_autorization_user(registration_user['email'], password)
        
        #проверка кода, состава ответа и значение ответа (комплексная проверка для вывода сразу всех проблем)
        assert action.check_answer(reqest, status_code, message_check) == 'Ok', ('Получено сообщение об ошибке, смотри результат проверки!')

