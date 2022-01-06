import string
import random


def create_random_string(length):
    string_pool = string.ascii_letters + string.digits

    result = ""
    for _ in range(length):
        result += random.choice(string_pool)

    return result