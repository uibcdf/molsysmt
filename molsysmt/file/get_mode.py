import os

def get_mode(filename):

    absolute_path = os.path.abspath(filename)

    if absolute_path in handler:
        return handler[absolute_path].mode
    else:
        return None

