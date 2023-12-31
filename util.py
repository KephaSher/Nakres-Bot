from time import time

# a timer that could be incorporated as a decorator
def timer(func):
    def inner(*args, **kwargs):
        starttime = time()
        val = func(*args, **kwargs)
        timespent = time() - starttime

        return (val, round(timespent, 3))
    return inner

def __main__(*args):
    return 0