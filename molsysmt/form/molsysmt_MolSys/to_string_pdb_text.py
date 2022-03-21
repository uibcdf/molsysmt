from .is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_string_pdb_text(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates, check=False)

    return tmp_item


