import os

def is_closed(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import handler

    return absolute_path not in handler

