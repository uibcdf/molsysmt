from .molmod import MolMod as _MolMod

def from_mdtraj(item=None, selection=None, frames=None, syntaxis='mdtraj'):

    from .io_trajectory import from_mdtraj_Trajectory as _from_mdtraj_Trajectory
    from .io_topology import from_mdtraj_Topology as _from_mdtraj_Topology

    tmp_molmod_item = _MolMod()
    tmp_molmod_item.topology = _from_mdtraj_Topology(item.topology, selection=selection,
                                                     syntaxis='mdtraj')
    tmp_molmod_item.trajectory = _from_mdtraj_Trajectory(item, selection=selection, frames=frames,
                                                        syntaxis=syntaxis)
    tmp_molmod_item.topography = None

    return tmp_molmod_item

def to_mdtraj_Trajectory(item=None, selection=None, frames=None, syntaxis='mdtraj'):

    from mdtraj import Trajectory as _mdtraj_Trajectory
    tmp_mdtraj_trajectory_item = _mdtraj_Trajectory(item.coordinates,item.topology_mdtraj)
    tmp_mdtraj_trajectory_item.unitcell_vectors = _np.ascontiguousarray(item.box)
    tmp_mdtraj_trajectory_item.time = _np.ascontiguousarray(item.time)
    del(_mdtraj_Trajectory)

    return tmp_item

def to_mdtraj(item=None, selection=None, frames=None, syntaxis='mdtraj'):

    return to_mdtraj_Trajectory(item, selection=selection, frames=frames, syntaxis=syntaxis)


def from_pdb(item=None,topology=None,selection=None,frames=None,syntaxis='mdtraj'):

    from .io_topology import from_pdb as _topology_from_pdb
    from .io_trajectory import from_pdb as _trajectory_from_pdb

    if topology is None:
        topology=item

    tmp_item =_MolMod()
    tmp_item.topology = _topology_from_pdb(item, selection=selection, syntaxis=syntaxis)
    tmp_item.trajectory = _trajectory_from_pdb(item, selection=selection, frames=frames,
                                               syntaxis=syntaxis)
    tmp_item.topography = None
    tmp_item.structure = None

    tmp_item.trajectory.topology = tmp_item.topology
    tmp_item.trajectory.structure = tmp_item.structure
    tmp_item.trajectory.topography = tmp_item.topography

    return tmp_item


def from_xtc(item=None,topology=None,selection=None,frames=None,syntaxis='mdtraj'):

    from .io_structure import from_gromacs_Topology as _structure_from_gromacs_Topology
    from .io_topology import from_molmod_Structure as _topology_from_molmod_Structure
    from .io_trajectory import from_xtc as _from_xtc

    tmp_item =_MolMod()
    tmp_item.structure = _structure_from_gromacs_Topology(topology)
    tmp_item.topology = _topology_from_molmod_Structure(tmp_item.structure)
    tmp_item.trajectory = _from_xtc(item, topology=tmp_item.topology, selection=selection, frames=frames, syntaxis=syntaxis)
    tmp_item.topography = None

    tmp_item.trajectory.topology = tmp_item.topology
    tmp_item.trajectory.structure = tmp_item.structure
    tmp_item.trajectory.topography = tmp_item.topography

    return tmp_item

