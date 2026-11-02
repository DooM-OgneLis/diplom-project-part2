import random
from faker import Faker
from data import Constant

fake = Faker()

def password_generator():
    """Генерирует случайный пароль (только буквы и цифры)"""
    generated_password = fake.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
    return generated_password

def name_generator():
    """Генерирует случайное имя"""
    generated_name = fake.first_name()
    return generated_name

def email_generator():
    """Генерирует случайный пароль (только буквы и цифры)"""
    generated_email = fake.email(safe=False, domain=random.choice(Constant.PST_DOMAIN))
    return generated_email

def random_in_list(list):
    return random.choice(list)