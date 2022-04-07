from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_PDBFile import is_openmm_PDBFile

def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', syntaxis='MolSysMT'):

    if check:

        try:
            is_openmm_PDBFile(item)
        except:
            raise WrongFormError('openmm.PDBFile')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item)

    return tmp_item

