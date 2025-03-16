from time import ticks_ms

enable = False

def log(*args, **kwargs):
    if not enable:
        return
    print('[' + str(ticks_ms()) + ']', *args, **kwargs)