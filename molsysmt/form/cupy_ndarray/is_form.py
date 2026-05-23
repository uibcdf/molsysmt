import numpy as np

def is_form(item):
    if item is None:
        return False

    val = item
    # Safe attribute check to see if item is a quantity without calling pyunitwizard functions
    if hasattr(item, 'unit') and hasattr(item, 'value'):
        val = item.value

    val_type_str = str(type(val))
    if 'cupy' in val_type_str and 'ndarray' in val_type_str:
        shape = np.shape(val)
        if len(shape) in (1, 2, 3) and shape[-1] == 3:
            return True
    return False
