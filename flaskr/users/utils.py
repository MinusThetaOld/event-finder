import random


def generate_token(size: int):
    sample_string = 'qwertyuioplkjhgfdsazxcvbnm1234567890'
    result = ''.join((random.choice(sample_string)) for x in range(size)) 
    return result
