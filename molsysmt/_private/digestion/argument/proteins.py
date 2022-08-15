from molsysmt._private.exceptions import ArgumentError

def digest_proteins(proteins, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(proteins, (bool, int)):
            return proteins
    if caller=='molsysmt.basic.contains.contains':
        if isinstance(proteins, (bool, int)):
            return proteins
        elif proteins is None:
            return None

    raise ArgumentError('proteins', value=proteins, caller=caller, message=None)

