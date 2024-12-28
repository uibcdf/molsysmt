from molsysmt._private.exceptions import ArgumentError

def digest_shape(shape, caller=None):

    if caller.endswith('get_box_with_shape'):
        if isinstance(shape, str):
            from .box_shape import _box_shape_values
            if shape.lower() in _box_shape_values:
                return shape.lower()

    raise ArgumentError('shape', value=shape, caller=caller, message=None)

