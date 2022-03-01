from .exceptions import NotImplementedMethodError
from .lists_and_tuples import is_list_or_tuple

def digest_molecular_system(molecular_system):

    from molsysmt.basic import is_a_molecular_system

    if is_a_molecular_system(molecular_system):
        return molecular_system
    else:
        raise NotImplementedMethodError()

