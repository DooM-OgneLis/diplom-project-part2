import allure
import pytest
import API.create_order as CO
from data import API, Request, IgnoreList

class TestOrders:
    @allure.title("Проверка создания заказа без авторизации на сайте")
    @pytest.mark.parametrize(
        'count, pattern, code',
        [[3, 'no_authorization', 200],[0,  'empty', 400]],
        ids = ['create_order_success','create_order_empty']
    )
    def test_create_order_in_no_login_user(self, count, pattern, code):
        action = CO.CreateOrder()

        message_check = Request.CREATE_ORDER[pattern]

        reqest = action.create_order(count)

        allure.dynamic.description(
            f"Отправить запрос POST на создание заказа.\n"
            f"Действие: отправка POST с данными: выбрать {count} ингредиентов начиная с булочки и отправить на {API.CREATE_ORDER}.\n"
            f"Ожидаемый результат: получен статус код {code} с сообщением {message_check}."
        )

        assert action.check_answer(reqest, code, message_check, IgnoreList.ORDER) == 'Ok'

    @allure.title("Проверка создания заказа с авторизацией на сайте")
    @pytest.mark.parametrize(
        'count, pattern, code',
        [[3, 'authorization', 200],[0,  'empty', 400]],
        ids = ['create_order_success','create_order_empty']
    )
    def test_create_order_in_login_user(self, registration_data, count, pattern, code):
        action = CO.CreateOrder()
        
        message_check = Request.CREATE_ORDER[pattern]

        reqest = action.create_order(count, registration_data['accessToken'])

        allure.dynamic.description(
            f"Отправить запрос POST на создание заказа.\n"
            f"Действие: отправка POST с данными: выбрать {count} ингредиентов начиная с булочки и отправить на {API.CREATE_ORDER} с токеном авторизации {registration_data['accessToken']}.\n"
            f"Ожидаемый результат: получен статус код {code} с сообщением {message_check}."
        )

        assert action.check_answer(reqest, code, message_check, IgnoreList.ORDER) == 'Ok'

    @allure.title("Проверка наличия всех полей в ответе при авторизованном пользователе")
    def test_create_order_in_login_user_check_key_list(self, registration_data):
        action = CO.CreateOrder()

        message_check = Request.CREATE_ORDER['authorization']

        reqest = action.create_order(2, registration_data['accessToken'])

        allure.dynamic.description(
                    f"Отправить запрос POST на создание заказа.\n"
                    f"Действие: отправка POST с данными: выбрать 2 ингредиентов начиная с булочки и отправить на {API.CREATE_ORDER} с токеном авторизации {registration_data['accessToken']}.\n"
                    f"Ожидаемый результат: получен статус код 200 с сообщением {message_check}, все поля ответа присутствуют."
                )

        assert action.request_mesage_key_check(set(reqest.json().keys()), set(message_check.keys()))[0] == 'Ok'
        assert action.request_mesage_key_check(set(reqest.json()["order"].keys()), set(message_check["order"].keys()))[0] == 'Ok'
        assert action.request_mesage_key_check(set(reqest.json()["order"]["ingredients"][0].keys()), set(message_check["order"]["ingredients"][0].keys()))[0] == 'Ok'
        assert action.request_mesage_key_check(set(reqest.json()["order"]["owner"].keys()), set(message_check["order"]["owner"].keys()))[0] == 'Ok'

    @allure.title("Проверка создания заказа с авторизацией на сайте и некорректным хешем ингредиен")
    def test_create_order_in_login_user(self, registration_data):
        action = CO.CreateOrder()

        action.data_ingredients['bun'] = ['1234e12124521']

        reqest = action.create_order(1, registration_data['accessToken'])

        allure.dynamic.description(
            f"Отправить запрос POST на создание заказа.\n"
            f"Действие: отправка POST с данными: выбрать некорректный кэш ингредиента и отправить на {API.CREATE_ORDER} с токеном авторизации {registration_data['accessToken']}.\n"
            f"Ожидаемый результат: получен статус код 500 internal Server Error."
        )

        assert action.request_code_check(reqest.status_code, 500)[0] == 'Ok'