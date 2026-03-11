from pathlib import Path
import os


def is_form(item):
    if isinstance(item, Path):
        item = str(item)

    if isinstance(item, str) and item.endswith('.molsys.yaml'):
        if not os.path.isfile(item):
            return True
        return True

    return False
