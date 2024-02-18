from molsysmt._private.exceptions import ArgumentError

def digest_bonded_atoms_pairs(bonded_atoms_pairs, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bonded_atoms_pairs, bool):
            return bonded_atoms_pairs

    raise ArgumentError('bonded_atoms_pairs', value=bonded_atoms_pairs, caller=caller, message=None)

