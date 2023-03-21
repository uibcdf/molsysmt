from molsysmt._private.exceptions import ArgumentError

def digest_from_molecular_system(from_molecular_system, caller=None):

    from molsysmt.basic import is_a_molecular_system

    if is_a_molecular_system(from_molecular_system):
        return from_molecular_system

    raise ArgumentError('from_molecular_system', value=from_molecular_system, caller=caller, message=None)
