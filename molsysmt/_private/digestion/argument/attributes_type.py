from ...exceptions import ArgumentError
from ...variables import is_all

def digest_attributes_type(attributes_type, caller=None):

    if caller=='molsysmt.basic.compare.compare':

        if attributes_type is None:
            return None
        elif is_all(attributes_type):
            return 'all'
        elif isinstance(attributes_type, str):
            if attributes_type.lower() in ['topological', 'structural', 'mechanical']:
                return attributes_type.lower()

    raise ArgumentError('attributes_type', value=attributes_type, caller=caller, message=None)

