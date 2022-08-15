from molsysmt._private.exceptions import ArgumentError

def digest_molecular_system_B(molecular_system_B, caller=None):

    from .molecular_system import digest_molecular_system

    try:
        return digest_molecular_system(molecular_system_B, caller=caller)
    except:
        raise ArgumentError(molecular_system_B, value=molecular_system_B, caller=caller, message=None)

