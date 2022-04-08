from .is_string_pdb_text import is_string_pdb_text
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', check=True):

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

    from io import StringIO
    from openmm.app.pdbfile import PDBFile
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFile(tmp_item)

    return tmp_item

