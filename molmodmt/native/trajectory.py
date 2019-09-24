import numpy as _np
from simtk import unit as _unit
from molmodmt.lib import box as _libbox
from molmodmt.lib import com as _libcom
from molmodmt.utils.exceptions import *
from copy import deepcopy

# Tiene que haber una manera automatica con f2py dar siempre de salida Ccontiguous_np.arrays

# Un frame tiene: step, time, coordinates, cell

class Trajectory():

    def __init__(self, filename=None):

        self.length_units = _unit.nanometers
        self.time_units = _unit.picoseconds

        self.step  = None
        self.time  = None
        self.coordinates = None # ndarray with shape=(n_frames, n_atoms, 3) and dtype=float
                                # and order=F, with units nanometers
        self.box  = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'
                          # cell is the matrix with the vectors

        self.box_shape   = None #
        self.n_frames = 0
        self.n_atoms = 0

        from .trajectory_file import TrajectoryFile
        self.file = TrajectoryFile(filename=filename)
        self.box_shape = self.file.box_shape

    def _set_frames(self, step=None, time=None, coordinates=None, box=None):

        self.coordinates = coordinates.in_units_of(self.length_units)
        self.time  = time.in_units_of(self.time_units)
        self.step  = step
        self.box  = box.in_units_of(self.length_units)

        if box is not None:
            if box[0] is None:
                self.box = None

        if self.coordinates is not None:
            self.n_frames = self.coordinates.shape[0]
            self.n_atoms = self.coordinates.shape[1]

        ii = self.coordinates
        if ii is not None:
            if _np.isfortran(ii)==False:
                ii=_np.asfortranarray(ii)

        ii = self.box
        if ii is not None:
            if _np.isfortran(ii)==False:
                ii=_np.asfortranarray(ii)

        ii = self.time
        if ii is not None:
            if _np.isfortran(ii)==False:
                ii=_np.asfortranarray(ii)

        ii = self.step
        if ii is not None:
            if _np.isfortran(ii)==False:
                ii=_np.asfortranarray(ii)

        pass

    def get_box_lengths(self):

        from molmodmt.utils.pbc import get_box_lengths as _get_box_lengths

        lengths = _get_box_lengths(self.box)

        return lengths

    def get_box_angles(self):

        from molmodmt.utils.pbc import get_box_angles as _get_box_angles

        angles = _get_box_angles(self.box)

        return angles

    def load_frames (self, frame_indices=None, atom_indices=None):

        from molmodmt import get

        if atom_indices == 'all':
            atom_indices = self.atom_indices

        step, time, coordinates, box = get(self.file.mount_point, element='atom',
                indices=atom_indices, frame_indices=frame_indices, frames=True)

        self._set_frames(step, time, coordinates, box)
        self.file.atom_indices = atom_indices
        del(coordinates, time, step, box)

        pass

    #def cell2box(self):
    #    self.box,self.volume,self.orthogonal=_libbox.cell2box(self.cell, self.n_frames)
    #    pass

    #def box2cell(self):
    #    self.cell,self.volume,self.orthogonal=_libbox.box2cell(self.box, self.n_frames)
    #    pass

    #def box2invbox(self):
    #    self.invbox=_libbox.box2invbox(self.box, self.n_frames)
    #    pass

    #def extract(self, atom_indices=None):

    #    tmp_item=deepcopy(self)
    #    tmp_item.coordinates=tmp_item.coordinates[:,atom_indices,:]
    #    tmp_item.n_atoms=len(atom_indices)

    #    return tmp_item

    #def iterload(self, chunk=100, stride=1, skip=0, atom_indices=None):

    #    atom_indices = None

    #    if selection is None:
    #        if self.selection_mdtraj is not None:
    #            atom_indices = self._atom_indices_mdtraj
    #    else:
    #        from molmodmt.multitool import select as _select
    #        atom_indices = _select(self.topology_mdtraj,selection,syntaxis)

    #    from mdtraj import iterload as _mdtraj_iterload
    #    tmp_top = self.topology_mdtraj

    #    iterator = _mdtraj_iterload(self.filename, top=tmp_top, chunk=chunk,
    #                                            stride=stride, atom_indices=atom_indices)

    #    while True:
    #        try:
    #            tmp_mdtraj = next(iterator)
    #        except StopIteration:
    #            return
    #        self._import_mdtraj_data(tmp_mdtraj)
    #        if atom_indices is not None:
    #            self._import_mdtraj_topology(tmp_mdtraj)
    #        del(tmp_mdtraj)
    #        yield

