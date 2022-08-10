from molsysmt._private.exceptions import ArgumentError

def digest_molecular_system_2(molecular_system_2, caller=None):

    from .molecular_system import digest_molecular_system

    if molecular_system_2 is None:
        return None

    try:
        return digest_molecular_system(molecular_system_2, caller=caller)
    except:
        raise ArgumentError(molecular_system_2, value=molecular_system_2, caller=caller, message=None)

