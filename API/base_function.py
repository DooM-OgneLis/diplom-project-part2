import allure

class BaseFunction:

    @allure.step('Проверить код запроса')
    def request_code_check(self, request_code, expected_code: int):
        if request_code == expected_code:
            return {0:'Ok'}
        else: return f'{request_code} != {expected_code}'

    @allure.step('Проверить тело запроса на соответствие полей')
    def request_mesage_key_check(self, request_js, data_request):
        msg_return = {0:'Ok'} #заготовка ответа
        #сравнение ключей ответа с ожидаемым списком
        missing_keys = list(request_js - data_request)
        extra_keys = list(data_request - request_js)
        if len(missing_keys) > 0 or len(extra_keys) > 0:
            msg_return['keys_list'] = f'не соответствует: нет: {missing_keys} | другие: {extra_keys}'
            msg_return[0] = 'Err'
        
        return msg_return

    @allure.step('Проверить тело запроса на соответствие значений')
    def request_mesage_check(self, request_js,  data_request: dict, ignore_list: list = []):
        msg_return = {0:'Ok'}#заготовка ответа
        #сравнение значений ответа с ожидаемым списком

        check_list = set(request_js.keys()) & set(data_request.keys())
        for key in check_list:
            if key in ignore_list:
                continue  # пропускаем проверку значения

            if request_js[key] != data_request[key]:
                msg_return[key] = f'{request_js[key]} != {data_request[key]}'
                msg_return[0] = 'Err'

        return msg_return

    @allure.step('Общая проверка соответствия кода и значений сообщения')
    def check_answer(self, request, expected_code, data_request: dict, ignore_list: list = []):
        check_list = {}
        check_list['code'] = self.request_code_check(request.status_code, expected_code)
        check_list['key'] = self.request_mesage_key_check(set(request.json().keys()), set(data_request.keys()))
        check_list['msg'] = self.request_mesage_check(request.json(), data_request, ignore_list)

        if check_list['code'][0] != 'Ok' or check_list['key'][0] != 'Ok' or check_list['msg'][0] != 'Ok':
            return check_list
        else: 
            return 'Ok'

    @allure.step('сравнение токена доступа')
    def check_token(self, request_token, chek_token):
        check = ''
        if request_token == chek_token:
            check = 'identical'
        else:
            check = 'different'
        return {0:check}

    @allure.step('общая проверка токенов')
    def check_tokens(self, request, data_chek, update_token: bool = False):
        check_list = {}
        check = 'identical'
        if update_token:
            check = 'different'
        check_list['access_token'] = self.check_token(request['accessToken'], data_chek['accessToken'])
        check_list['refresh_token'] = self.check_token(request['refreshToken'], data_chek['refreshToken'])

        if check_list['access_token'][0] != check or check_list['refresh_token'][0] != check:
            return check_list
        else: 
            return 'Ok'
