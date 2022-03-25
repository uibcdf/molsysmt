from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolSys import is_molsysmt_MolSys

def to_openmm_Topology(item, atom_indices='all', structure_indices='all', check=True):

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
    from . import get_box_from_system
    from ..molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology

    tmp_item = to_molsysmt_Topology(item, check=False)
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item, box=box, atom_indices=atom_indices, check=False)

    return tmp_item

