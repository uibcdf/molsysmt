from molsysmt._private.smonitor import ArgumentError

def digest_remove_bonds(remove_bonds, caller=None):

    if remove_bonds is None:
        return None

    from .indices import arg_digest_indices

    try:
        return digest_indices(remove_bonds, caller=caller)
    except:
        raise ArgumentError('remove_bonds', value=remove_bonds, caller=caller, message=None)

