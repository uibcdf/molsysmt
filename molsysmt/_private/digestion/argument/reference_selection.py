from molsysmt._private.exceptions import ArgumentError

def digest_reference_selection(reference_selection, syntax="MolSysMT", caller=None):

    from .selection import digest_selection

    try:
        return digest_selection(reference_selection, syntax=syntax, caller=caller)
    except:
        raise ArgumentError('reference_selection', value=reference_selection, caller=caller, message=None)

