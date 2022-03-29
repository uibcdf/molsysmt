from .is_string_pdb_text import is_string_pdb_text
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_openmm_Modeller as openmm_PDBFile_to_openmm_Modeller

    tmp_item = to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_PDBFile_to_openmm_Modeller(tmp_item, check=False)

    return tmp_item

