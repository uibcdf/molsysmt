from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form={}

def to_mdtraj(item):

    import simtk.unit as unit
    from mdtraj.core.trajectory import Trajectory as mdtraj_trajectory
    from mdtraj.core.topology import Topology as mdtraj_topology

    return mdtraj_trajectory(item.positions/unit.nanometers,mdtraj_topology.from_openmm(item.topology))
