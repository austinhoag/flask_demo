# app/tasks.py
from . import cel

@cel.task()
def reverse(name):
    import time
    return name[::-1]