from molsysmt._private.smonitor import ArgumentError

def digest_molecular_system_A(molecular_system_A, caller=None):

    from .molecular_system import digest_molecular_system

    try:
        return digest_molecular_system(molecular_system_A, caller=caller)
    except Exception:
        raise ArgumentError("molecular_system_A", value=molecular_system_A, caller=caller, message=None)
