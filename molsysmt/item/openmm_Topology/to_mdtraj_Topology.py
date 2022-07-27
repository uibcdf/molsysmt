from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_mdtraj_Topology(item, atom_indices='all'):

    if check:

        digest_item(item, 'openmm.Topology')
        atom_indices = digest_atom_indices(atom_indices)

    try:
        from mdtraj.core.topology import Topology as mdtraj_Topology
    except:
        raise LibraryNotFoundError('MDTraj')

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)
    tmp_item = mdtraj_Topology.from_openmm(tmp_item)

    return tmp_item


