import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str

def get_random_number(length):
    # choose from all lowercase letter
    numbers = string.digits
    #print(numbers)
    result_str = ''.join(random.choice(numbers) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str