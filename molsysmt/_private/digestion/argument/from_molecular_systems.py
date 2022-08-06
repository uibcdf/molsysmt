from molsysmt._private.exceptions import ArgumentError

def digest_from_molecular_systems(from_molecular_systems, caller=None):

    from molsysmt.basic import are_multiple_molecular_systems
    from molsysmt.basic import is_molecular_system

    if caller=='add':
        if is_molecular_system(from_molecular_systems):
            return from_molecular_systems
        elif are_multiple_molecular_systems(from_molecular_systems):
            return from_molecular_systems
        else:
            raise ArgumentError(from_molecular_systems, caller=caller, message=None)
    else:

        if not are_multiple_molecular_systems(from_molecular_systems):
            raise ArgumentError(from_molecular_systems, caller=caller, message=None)

        return from_molecular_systems

