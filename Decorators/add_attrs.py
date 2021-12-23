from functools import wraps

def add_attrs(**kwargs):
    def decorate(func):
        for k, v in kwargs.items():
            setattr(func, k, v)
        return func
    return decorate