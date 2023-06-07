from pathlib import PosixPath

def is_form(item):

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        output = (item.endswith('.prmtop') or item.endswith('.parm7'))

    return output

