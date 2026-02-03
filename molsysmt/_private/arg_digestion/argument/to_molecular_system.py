from molsysmt._private.exceptions import ArgumentError

def digest_to_molecular_system(to_molecular_system, caller=None):

    from molsysmt.basic import is_a_molecular_system

    if not is_a_molecular_system(to_molecular_system):
        raise ArgumentError(to_molecular_system, value=to_molecular_system, caller=caller, message=None)

    return to_molecular_system

