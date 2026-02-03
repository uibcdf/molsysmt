from molsysmt._private.exceptions import ArgumentError

_box_shape_values = [
    "cubic",
    "truncated octahedral",
    "rhombic dodecahedral",
]

def digest_box_shape(box_shape, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(box_shape, bool):
            return box_shape
        else:
            raise ArgumentError('box_shape', value=box_shape, caller=caller, message=None)

    if isinstance(box_shape, str):
        if box_shape.lower() in _box_shape_values:
            return box_shape.lower()

    raise ArgumentError('box_shape', value=box_shape, caller=caller, message=None)
