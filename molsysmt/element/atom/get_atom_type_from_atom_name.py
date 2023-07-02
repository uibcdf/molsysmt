from molsysmt._private.digestion import digest
from .names import atom, atom_type

@digest()
def get_atom_type_from_atom_name(atom_name):
    """
    To be written soon...
    """

    return atom_type[atom[atom_name]]

