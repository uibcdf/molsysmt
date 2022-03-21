from .is_molsysmt_Topology import is_molsysmt_Topology
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_string_pdb_text(item, coordinates, box, atom_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_Topology
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item =  to_openmm_Topology(item, box, atom_indices=atom_indices, check=False)
    tmp_item =  openmm_Topology_to_string_pdb_text(tmp_item, coordinates, check=False)

    return tmp_item

