from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_mdtraj_Topology(item, atom_indices='all'):

    try:
        from mdtraj.core.topology import Topology as mdtraj_Topology
    except:
        raise LibraryNotFoundError('MDTraj')

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    return tmp_item

def _to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Topology(item, atom_indices=atom_indices)

