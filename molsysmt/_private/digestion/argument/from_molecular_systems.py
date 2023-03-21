from molsysmt._private.exceptions import ArgumentError

def digest_from_molecular_systems(from_molecular_systems, caller=None):

    from molsysmt.basic import are_multiple_molecular_systems

    if are_multiple_molecular_systems(from_molecular_systems):
        return from_molecular_systems

    raise ArgumentError('from_molecular_systems', value=from_molecular_systems, caller=caller, message=None)

