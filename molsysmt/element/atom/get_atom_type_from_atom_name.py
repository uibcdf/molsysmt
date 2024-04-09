from molsysmt._private.digestion import digest
from .names import atom as atom_type_from_name

@digest()
def get_atom_type_from_atom_name(atom_name):
    """
    To be written soon...
    """

    try:
        return atom_type_from_name[atom_name]
    except:
        print(f'The atom_name {atom_name} was not recognized')
        return 'ANK'
        #raise ValueError('Atom name '+atom_name+' has not known atom type.')

