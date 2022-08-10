from molsysmt._private.exceptions import ArgumentError

def digest_reference_molecular_system(reference_molecular_system, caller=None):

    if reference_molecular_system is None:
        return None

    from .molecular_system import digest_molecular_system

    try:
        return digest_molecular_system(reference_molecular_system, caller=caller)
    except:
        raise ArgumentError('reference_molecular_system', value=reference_molecular_system, caller=caller, message=None)

