from molsysmt._private.exceptions import ArgumentError

def digest_bonded_atoms(bonded_atoms, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bonded_atoms, bool):
            return bonded_atoms

    raise ArgumentError('bonded_atoms', value=bonded_atoms, caller=caller, message=None)

