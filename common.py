import generator

#в данном файле хранятся повторяющиеся модули в тестах и модули формирующие списки данных для теста
    
def gen_list_register():
    email = generator.email_generator()
    password = generator.password_generator()
    name = generator.name_generator()
    return {
            'email': email,
            'password': password,
            'name': name
        }


