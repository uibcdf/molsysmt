from molsysmt._private.digestion import digest
from .names import atom, atom_type

@digest()
def get_atom_type_from_atom_name(atom_name):
    """
    To be written soon...
    """

    try:
        return atom_type[atom[atom_name]]
    except:
        raise ValueError('Atom name '+atom_name+' has not known atom type.')

