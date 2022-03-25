from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_Topology import is_openmm_Topology

def to_mdtraj_Topology(item, atom_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    try:
        from mdtraj.core.topology import Topology as mdtraj_Topology
    except:
        raise LibraryNotFoundError('MDTraj')

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, check=False)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    return tmp_item


