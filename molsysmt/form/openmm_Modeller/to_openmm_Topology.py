from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import LibraryNotFound
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_openmm_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_openmm_Modeller(item)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import extract

    tmp_item = item.getTopology()
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

