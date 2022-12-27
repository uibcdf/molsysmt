import os

def is_opened(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import handler

    return absolute_path in handler

