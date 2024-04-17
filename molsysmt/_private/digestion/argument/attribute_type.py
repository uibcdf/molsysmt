from ...exceptions import ArgumentError
from ...variables import is_all

def digest_attribute_type(attribute_type, caller=None):

    if caller=='molsysmt.basic.compare.compare':

        if attribute_type is None:
            return None
        elif is_all(attribute_type):
            return 'all'
        elif isinstance(attribute_type, str):
            if attribute_type.lower() in ['topological', 'structural', 'mechanical']:
                return attribute_type.lower()

    raise ArgumentError('attribute_type', value=attribute_type, caller=caller, message=None)

