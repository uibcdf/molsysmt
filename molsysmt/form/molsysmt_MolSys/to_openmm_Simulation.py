from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolSys import is_molsysmt_MolSys

def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', check=True):

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
    from ..openmm_Topology import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, check=False)

    return tmp_item

