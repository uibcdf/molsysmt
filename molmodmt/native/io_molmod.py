from .molmod import MolMod as _MolMod
from os import remove as _remove

def from_mdtraj_Trajectory(item=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    from .io_trajectory import from_mdtraj_Trajectory as _from_mdtraj_Trajectory
    from .io_topology import from_mdtraj_Topology as _from_mdtraj_Topology

    tmp_molmod_item = _MolMod()
    tmp_molmod_item.topology = _from_mdtraj_Topology(item.topology, selection=selection,
                                                     syntaxis='mdtraj')
    tmp_molmod_item.trajectory = _from_mdtraj_Trajectory(item, selection=selection,
                                                         frame_indices=frame_indices,
                                                        syntaxis=syntaxis)
    tmp_molmod_item.topography = None

    return tmp_molmod_item

def from_mdtraj(item=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    return from_mdtraj_Trajectory(item=item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

def to_mdtraj_Topology(item=None, selection=None, syntaxis='mdtraj'):

    tmp_item = item.topology
    if selection is not None:
        from molmodmt import extract as _extract
        tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj_Trajectory(item=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    from mdtraj import Trajectory as _mdtraj_Trajectory
    from numpy import ascontiguousarray as _ascontiguousarray
    tmp_item = _mdtraj_Trajectory(item.trajectory.coordinates,item.topology)
    tmp_item.unitcell_vectors = _ascontiguousarray(item.trajectory.box)
    tmp_item.time = _ascontiguousarray(item.trajectory.time)

    return tmp_item

def to_mdtraj(item=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    return to_mdtraj_Trajectory(item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

def from_openmm_Modeller(item=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    from .io_trajectory import from_openmm_Modeller as trajectory_from_mdtraj_Trajectory
    from .io_topology import from_openmm_Modeller as topology_from_mdtraj_Topology

    tmp_item = _MolMod()
    tmp_item.topology = topology_from_mdtraj_Topology(item, selection=selection, syntaxis='mdtraj')
    tmp_item.trajectory = trajectory_from_mdtraj_Trajectory(item, selection=selection,
                                                            frame_indices=frame_indices,
                                                            syntaxis=syntaxis)
    tmp_item.topography = None
    return tmp_item

def from_pdbid(item=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    from molmodmt.utils.miscellanea import download_pdb as _download_pdb
    tmp_file=_download_pdb(item)
    tmp_item=from_pdb(tmp_file, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)
    _remove(tmp_file)
    return tmp_item

def from_pdb(item=None,topology=None,selection=None,frame_indices=None,syntaxis='mdtraj'):

    from molmodmt import convert as _convert
    from .io_topology import from_mdtraj as _topology_from_mdtraj
    from .io_trajectory import from_mdtraj as _trajectory_from_mdtraj

    if topology is None:
        topology=item

    tmp_item_mdtraj = _convert(item, 'mdtraj', selection=selection, syntaxis=syntaxis)

    tmp_item =_MolMod()
    tmp_item.topology = _topology_from_mdtraj(tmp_item_mdtraj)
    tmp_item.trajectory = _trajectory_from_mdtraj(tmp_item_mdtraj, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    tmp_item.trajectory.topology = tmp_item.topology
    tmp_item.trajectory.structure = tmp_item.structure
    tmp_item.trajectory.topography = tmp_item.topography

    return tmp_item

def to_pdb(item=None, filename=None, selection=None, frame_indices=None, syntaxis='mdtraj'):

    from molmodmt import convert as _convert
    tmp_item = _convert(item, 'mdtraj', selection=selection, syntaxis=syntaxis)
    return _convert(tmp_item, filename, frame_indices=frame_indices)

def from_xtc(item=None,topology=None,selection=None,frame_indices=None,syntaxis='mdtraj'):

    from .io_structure import from_gromacs_Topology as _structure_from_gromacs_Topology
    from .io_topology import from_molmod_Structure as _topology_from_molmod_Structure
    from .io_trajectory import from_xtc as _from_xtc

    tmp_item =_MolMod()
    tmp_item.structure = _structure_from_gromacs_Topology(topology)
    tmp_item.topology = _topology_from_molmod_Structure(tmp_item.structure)
    tmp_item.trajectory = _from_xtc(item, topology=tmp_item.topology, selection=selection,
                                    frame_indices=frame_indices, syntaxis=syntaxis)
    tmp_item.topography = None

    tmp_item.trajectory.topology = tmp_item.topology
    tmp_item.trajectory.structure = tmp_item.structure
    tmp_item.trajectory.topography = tmp_item.topography

    return tmp_item

