from molsysmt._private.exceptions import ArgumentError

def digest_from_molecular_systems(from_molecular_systems, caller=None):

    from molsysmt.basic import are_multiple_molecular_systems
    from molsysmt.basic import is_molecular_system

    if caller=='add':
        print('Esta dentro!')

    if not are_multiple_molecular_systems(molecular_systems):
        raise ArgumentError(molecular_systems, caller=caller, message=None)

    return molecular_systems
