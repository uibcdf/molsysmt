from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids3(item, atom_indices='all'):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_openmm_Topology

    tmp_item  = to_openm_Topology(item, atom_indices=atom_indices)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])

    return tmp_item

