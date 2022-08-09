from molsysmt._private.exceptions import ArgumentError

def digest_hydrogens(hydrogens, caller=None):

    if caller=='molsysmt.basic.contains.contains':
        if isinstance(hydrogens, (bool, int)):
            return hydrogens
        elif hydrogens is None:
            return None

    raise ArgumentError('hydrogens', value=hydrogens, caller=caller, message=None)

