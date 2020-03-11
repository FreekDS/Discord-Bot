from functools import wraps


def prune_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("called")
        return [i for i in func(*args, **kwargs) if i]

    return wrapper
