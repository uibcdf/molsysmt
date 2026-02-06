from molsysmt.exceptions import ArgumentError
from ...variables import is_all

_funcions_with_attribute_type = [
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.get_attributes.get_attributes',
]

def digest_attribute_type(attribute_type, caller=None):

    if caller in _funcions_with_attribute_type:

        if attribute_type is None:
            return None
        elif is_all(attribute_type):
            return 'all'
        elif isinstance(attribute_type, str):
            if attribute_type.lower() in ['topological', 'structural', 'mechanical']:
                return attribute_type.lower()

    raise ArgumentError('attribute_type', value=attribute_type, caller=caller, message=None)

