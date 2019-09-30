
#def from_mdtraj_Trajectory(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from .io_trajectory import from_mdtraj_Trajectory as _from_mdtraj_Trajectory
#    from .io_topology import from_mdtraj_Topology as _from_mdtraj_Topology
#    from .molmod import MolMod as _MolMod
#
#    tmp_molmod_item = _MolMod()
#    tmp_molmod_item.topology = _from_mdtraj_Topology(item.topology, selection=selection,
#                                                     syntaxis='mdtraj')
#    tmp_molmod_item.trajectory = _from_mdtraj_Trajectory(item, selection=selection,
#                                                         frame_indices=frame_indices,
#                                                        syntaxis=syntaxis)
#    tmp_molmod_item.topography = None
#
#    return tmp_molmod_item

#def from_mdtraj(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    return from_mdtraj_Trajectory(item=item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

#def to_mdtraj_Topology(item=None, selection='all', syntaxis='MDTraj'):
#
#    tmp_item = item.topology
#    if selection is not None:
#        from molmodmt import extract as _extract
#        tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
#    return tmp_item

#def to_mdtraj_Trajectory(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from mdtraj import Trajectory as _mdtraj_Trajectory
#    from numpy import ascontiguousarray as _ascontiguousarray
#    tmp_item = _mdtraj_Trajectory(item.trajectory.coordinates,item.topology)
#    tmp_item.unitcell_vectors = _ascontiguousarray(item.trajectory.box)
#    tmp_item.time = _ascontiguousarray(item.trajectory.time)
#
#    return tmp_item

#def to_mdtraj(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    return to_mdtraj_Trajectory(item, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

#def from_openmm_Modeller(item=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from .io_trajectory import from_openmm_Modeller as trajectory_from_mdtraj_Trajectory
#    from .io_topology import from_openmm_Modeller as topology_from_mdtraj_Topology
#    from .molmod import MolMod as _MolMod
#
#    tmp_item = _MolMod()
#    tmp_item.topology = topology_from_mdtraj_Topology(item, selection=selection, syntaxis='MDTraj')
#    tmp_item.trajectory = trajectory_from_mdtraj_Trajectory(item, selection=selection,
#                                                            frame_indices=frame_indices,
#                                                            syntaxis=syntaxis)
#    tmp_item.topography = None
#    return tmp_item

def from_pdb(item=None, topology=None, selection='all', frame_indices='all', syntaxis='MDTraj'):

    from molmodmt import select, convert
    from .molmod import MolMod

    if topology is None:
        topology = item

    atom_indices = select(item, selection=selection, syntaxis=syntaxis)

    print('si')

    tmp_item = MolMod()
    tmp_item.topology = convert(topology, 'molmodmt.Topology', selection=atom_indices)
    tmp_item.trajectory = convert(item, 'molmodmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    return tmp_item

def from_xtc(item=None, topology=None, selection='all', frame_indices='all', syntaxis='MDTraj'):

    from molmodmt import select, convert
    from .molmod import MolMod

    atom_indices = select(item, selection=selection, syntaxis=syntaxis)

    tmp_item = MolMod()
    tmp_item.topology = convert(topology, 'molmodmt.Topology', selection=atom_indices)
    tmp_item.trajectory = convert(item, 'molmodmt.Trajectory', atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    return tmp_item

def from_hdf5(item=None, topology=None, selection='all', frame_indices='all', syntaxis='MDTraj'):

    from molmodmt import select, convert
    from .molmod import MolMod

    if topology is None:
        topology = item

    atom_indices = select(item, selection=selection, syntaxis=syntaxis)

    tmp_item = MolMod()
    tmp_item.topology = convert(topology, 'molmodmt.Topology', selection=atom_indices)
    tmp_item.trajectory = convert(item, 'molmodmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    return tmp_item

#def to_pdb(item=None, filename=None, selection='all', frame_indices='all', syntaxis='MDTraj'):
#
#    from molmodmt import convert as _convert
#    tmp_item = _convert(item, 'mdtraj', selection=selection, syntaxis=syntaxis)
#    return _convert(tmp_item, filename, frame_indices=frame_indices)

