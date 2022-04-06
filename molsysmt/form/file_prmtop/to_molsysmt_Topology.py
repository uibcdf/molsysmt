from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Topology(item, atom_indices='all', check=True):

    if check:

        try:
            is_file_prmtop(item)
        except:
            raise WrongFormError('file:prmtop')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_openmm_Topology
    from ..openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    tmp_item = to_openmm_Topology(item, check=False)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, check=False)
    return tmp_item

