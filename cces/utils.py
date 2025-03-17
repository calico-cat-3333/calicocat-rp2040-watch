import os

def path_exist(path):
    try:
        os.stat(path)
        return True
    except OSError as e:
        if e.errno == 2:
            return False

def is_file(path):
    if os.stat(path)[0] & 0xf000 == 0x4000:
        return False
    return True