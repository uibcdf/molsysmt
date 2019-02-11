from .molmod import MolMod as _MolMod

def from_mdtraj (item=None):

    from .io_trajectory import from_mdtraj_Trajectory as _from_mdtraj_Trajectory
    from .io_topology import from_mdtraj_Topology as _from_mdtraj_Topology

    tmp_molmod_item = _MolMod()
    tmp_molmod_item.trajectory = _from_mdtraj_Trajectory(item)
    tmp_molmod_item.topology = _from_mdtraj_Topology(item.topology)
    tmp_molmod_item.topography = None

    return tmp_molmod_item

