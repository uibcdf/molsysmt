from .is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_mdtraj_Topology(item, atom_indices='all', check=True):

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

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = to_molsysmt_Topology(item, check=False)
    tmp_item = molsysmt_Topology_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices, check=False)

    return tmp_item

