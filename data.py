class URL:
    STELLARBURGERS = 'https://stellarburgers.education-services.ru/'

class API:
    CREATE_USER = URL.STELLARBURGERS+'api/auth/register'
    AUTHORIZATION = URL.STELLARBURGERS+'api/auth/login'
    CREATE_ORDER = URL.STELLARBURGERS+'api/orders'
    INGREDIENTS = URL.STELLARBURGERS+'api/ingredients'

class Constant:
    PST_DOMAIN = ['ya.ru', 'yandex.ru', 'google.com', 'yahoo.com', 'mail.ru']

#макеты возвращаемых ответов для проведения проверки соответствия
class Request:
    CREATE_USER = {
        'Created': {
            "success": True,
            "user": {
                "email": None,
                "name": None
            },
            "accessToken": "#токен_доступа",
            "refreshToken": "#токен_обновления"
        },
        'double': {
            "success": False,
            "message": "User already exists"
        },
        'mandatory': {
            "success": False,
            "message": "Email, password and name are required fields"
        }
    }
    
    AUTHORIZATION ={
        'success': {
            "success": True,
            "accessToken": "#токен_доступа",
            "refreshToken": "#токен_обновления",
            "user": {
                "email": "",
                "name": ""
            }
        },
        'denite': {
            "success": False,
            "message": "email or password are incorrect"
        }
    }

    CREATE_ORDER = {
        'no_authorization':{
            "name": "",
            "order": {
                "number": 0
            },
            "success": True
        },
        'authorization': {
            "success": True,
            "name": "",
            "order": {
                "ingredients": [
                    {
                        "_id": "",
                        "name": "",
                        "type": "",
                        "proteins": 0,
                        "fat": 0,
                        "carbohydrates": 0,
                        "calories": 0,
                        "price": 0,
                        "image": "",
                        "image_mobile": "",
                        "image_large": "",
                        "__v": 0
                    }
                ],
                "_id": "",
                "owner": {
                    "name": "",
                    "email": "",
                    "createdAt": "",
                    "updatedAt": ""
                },
                "status": "created",
                "name": "",
                "createdAt": "",
                "updatedAt": "",
                "number": 0,
                "price": 0
            }
        },
        'hash_error':{},
        'empty':{
            "success": False,
            "message": "Ingredient ids must be provided"
        }
    }

class IgnoreList:
    TOKEN = ["accessToken", "refreshToken"]
    ORDER = ["name", "order"]