from .molmod import MolMod as _MolMod

def from_mdtraj(item=None):

    from .io_trajectory import from_mdtraj_Trajectory as _from_mdtraj_Trajectory
    from .io_topology import from_mdtraj_Topology as _from_mdtraj_Topology

    tmp_molmod_item = _MolMod()
    tmp_molmod_item.topology = _from_mdtraj_Topology(item.topology)
    tmp_molmod_item.trajectory = _from_mdtraj_Trajectory(item)
    tmp_molmod_item.topography = None

    return tmp_molmod_item

def to_mdtraj(item=None):

    from .io_trajectory import to_mdtraj_Trajectory as _to_mdtraj_Trajectory

    tmp_mdtraj_item = _to_mdtraj_Trajectory(item)

    return tmp_mdtraj_item

def from_xtc(item=None,topology=None,frames=None):

    from .io_structure import from_gromacs_Topology as _structure_from_gromacs_Topology
    from .io_topology import from_molmod_Structure as _topology_from_molmod_Structure
    from .io_trajectory import from_xtc as _from_xtc

    tmp_molmod_item =_MolMod()
    tmp_molmod_item.structure = _structure_from_gromacs_Topology(topology)
    tmp_molmod_item.topology = _topology_from_molmod_Structure(tmp_molmod_item.structure)
    tmp_molmod_item.trajectory = _from_xtc(item, topology = tmp_molmod_item.topology)
    tmp_molmod_item.topography = None

    return tmp_moldmod_item
