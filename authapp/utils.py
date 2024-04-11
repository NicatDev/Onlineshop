import random
import string
def createCode(title):
    code = title[0:2]

    for _ in range(5):  
        code += random.choice(string.ascii_letters)
    code += 'confirmationcode23fa-402'
    return code