import random

def code_generator(code = '100000'):
    new_code = ''
    for i in range(6):
        new_code += str(random.randint(0,9))
    if new_code != code:
        return new_code
    else:
        return code_generator(new_code)

