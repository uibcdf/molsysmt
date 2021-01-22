import numpy as _np
from .multitool import convert as _convert, extract as _extract, get as _get
from .tools.digest_inputs import _one_system as _digest_one_system
from .tools.digest_inputs import _coordinates as _digest_coordinates
from .lib import geometry as _libgeometry
from .tools.exceptions import *

def radius_of_gyration(item=None, selection=None, frame=None, engine='molsysmt'):

    if engine=='molsysmt':

        tmp_item, atom_indices, frame_indices = _digest_one_system(item, selection, frame,
                                                                      form='molsysmt.Trajectory')
        tmp_coors, tmp_n_frames, tmp_n_atoms = _digest_coordinates(tmp_item, atom_indices, frame_indices, form='molsysmt.Trajectory')
        masses = _get(tmp_item, selection=atom_indices, masses=True)
        rg = _libgeometry.radius_of_gyration(tmp_coors, masses,tmp_n_frames,tmp_n_atoms)
        del(tmp_item, atom_indices, frame_indices, tmp_coors, masses)

        return rg

    elif engine=='mdtraj':

        from mdtraj import compute_rg as _mdtraj_rg

        tmp_item1, atom_indices1, frame_indices1 = _digest_one_system(item, selection, frame,
                                                                      form='mdtraj.Trajectory')
        tmp_item1 = _extract(tmp_item1,atom_indices1)
        masses = _get(tmp_item1, masses=True)
        rg = _mdtraj_rg(tmp_item1,masses=_np.array(masses))
        del(tmp_item1, atom_indices1, frame_indices1, masses)

        return rg

    else:

        raise NotImplementedError(NotImplementedMessage)

