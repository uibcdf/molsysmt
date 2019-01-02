# import numpy as np

# from .aux_tools import normalize_set as _normalize_set
# from .aux_tools import normalize_system as _normalize_system
# from .aux_tools import normalize_selection as _normalize_selection
# from .aux_tools import not_implemented as _not_implemented

# def _complete_ref(ref_system=None, ref_trajectory=None, ref_topology=None, ref_frame_indices=None, ref_selection=None, ref_atom_indices=None,
#                   system=None, trajectory=None, topology=None, frame_indices=None, selection=None, atom_indices=None):

#     single_system=False

#     if ref_selection==None and ref_atom_indices==None:
#         ref_selection=selection
#         ref_atom_indices=atom_indices

#     if ref_system==None and ref_trajectory==None and ref_topology==None:
#         single_system=True

#     return single_system


def rmsd(ref_item=None, ref_select='All', ref_frame=0,
         item=None, select=None, frame='All',
         pbc=False, parallel=False, engine='native'):

    single_system = _complete_ref(ref_system, ref_trajectory, ref_topology, ref_frame_indices, ref_selection, ref_atom_indices,
                                  system, trajectory, topology, frame_indices, selection, atom_indices)

    native_system = import_system(system,trajectory,topology)

    if single_system:
        ref_native_system = native_system
    else:
        ref_native_system = import_system(ref_system,ref_trajectory,ref_topology)

    if engine=='self':

        _not_implemented(); pass

    pass

# def least_rmsd(ref_system=None, ref_trajectory=None, ref_topology=None, ref_frame_indices=0, ref_selection=None, ref_atom_indices=None,
#                system=None, trajectory=None, topology=None, frame_indices='All', selection=None, atom_indices=None,
#                pbc=False, parallel=False, engine='native'):

#     ref_system, ref_topology, ref_trajectory, ref_frame_indices, ref_atom_indices = _normalize_set(ref_system, ref_topology, ref_trajectory, ref_frame_indices, ref_selection, ref_atom_indices)
#     system, topology, trajectory, frame_indices, atom_indices = _normalize_set(system, topology, trajectory, frame_indices, selection, atom_indices)

#     if engine=='self':

#         _not_implemented()

#     elif engine=='mdtraj':

#         _not_implemented()

#     pass

# def least_rmsd_fit(ref_system=None, ref_trajectory=None, ref_topology=None, ref_frame_indices=0, ref_selection=None, ref_atom_indices=None,
#                    system=None, trajectory=None, topology=None, frame_indices='All', selection=None, atom_indices=None,
#                    pbc=False, in_place=True, rmsd=False, parallel=False, engine='native'):

#     ref_system, ref_topology, ref_trajectory, ref_frame_indices, ref_atom_indices = _normalize_set(ref_system, ref_topology, ref_trajectory, ref_frame_indices, ref_selection, ref_atom_indices)
#     system, topology, trajectory, frame_indices, atom_indices =_normalize_set(system, topology, trajectory, frame_indices, selection, atom_indices)

#     pass

