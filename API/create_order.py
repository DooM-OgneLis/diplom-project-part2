import requests
import allure
from API.base_function import BaseFunction
from data import API
import generator

class CreateOrder(BaseFunction):
    #запрос данных ингредиентов с сайта при инициализации класса
    @allure.step('инициализация объекта')
    def __init__(self):
        self.data_ingredients = {}
        self.data_ingredients = self.get_ingredients_list()

    @allure.step('формирование листа ингредиентов при инициализации')
    def get_ingredients_list(self):
        dict_data = {}
        request = requests.get(
                            API.INGREDIENTS
                        )
        
        list_full = request.json()
        list_ingredients_full = list_full['data']

        for index in list_ingredients_full:
            if index['type'] not in dict_data:
                dict_data[index['type']] = []
            dict_data[index['type']].append(index['_id'])

        return dict_data

    @allure.step('создание заказа')
    def create_order(self, num_ingredients:int, session_token = None):
        dict_ingredients = {}
        list_ingredients = []

        authorization = {}

        if session_token is not None:
            authorization['Authorization'] = session_token

        if num_ingredients != 0:
            list_ingredients.append(generator.random_in_list(self.data_ingredients['bun']))
            for n in range(num_ingredients - 1):
                list_ingredients.append(generator.random_in_list(self.data_ingredients['sauce']+self.data_ingredients['main']))
        
            dict_ingredients['ingredients'] = list_ingredients
        else:
            dict_ingredients = {}
        
        request = requests.post(
                            API.CREATE_ORDER,
                            json={'ingredients': list_ingredients},
                            headers=authorization
                        )

        return request


