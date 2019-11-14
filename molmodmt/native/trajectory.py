import numpy as _np
import molmodmt.utils.units as m3t_units
from molmodmt.lib import box as _libbox
from molmodmt.lib import com as _libcom
from molmodmt.utils.exceptions import *

# Tiene que haber una manera automatica con f2py dar siempre de salida Ccontiguous_np.arrays

# Un frame tiene: step, time, coordinates, cell

class Trajectory():

    def __init__(self, file_path=None, atom_indices='all', frame_indices='all'):

        self.step  = None
        self.time  = None
        self.coordinates = None # ndarray with shape=(n_frames, n_atoms, 3) and dtype=float
                                # and order=F, with units nanometers
        self.box  = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'
                          # cell is the matrix with the vectors
        self.atom_indices = None
        self.n_frames = 0
        self.n_atoms = 0

        if file_path is not None:
            self.load_frames_from_file(file_path=file_path, atom_indices=atom_indices, frame_indices=frame_indices)

    def _set_frames(self, atom_indices=None, step=None, time=None, coordinates=None, box=None):

        self.coordinates = coordinates.in_units_of(m3t_units.length)
        self.time  = time.in_units_of(m3t_units.time)
        self.step  = step
        self.box  = box.in_units_of(m3t_units.length)
        self.atom_indices = atom_indices

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

    def load_frames_from_file (self, file_path=None, atom_indices='all', frame_indices='all'):

        if file_path is not None:

            from .trajectory_file import TrajectoryFile
            self.file = TrajectoryFile(file_path=file_path)
            self.box_shape = self.file.box_shape


        step, time, coordinates, box = self.file.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)

        self._set_frames(atom_indices, step, time, coordinates, box)

        del(coordinates, time, step, box)

        pass

    def extract (self, atom_indices='all', frame_indices='all'):

        if atom_indices is 'all' and frame_indices is 'all':

            tmp_item = duplicate(self)

        else:

            from copy import deepcopy

            tmp_item = Trajectory()

            tmp_item.step = self.step[frame_indices]
            tmp_item.time = self.time[frame_indices]
            tmp_item.box = self.box[frame_indices]
            tmp_item.coordinates = self.coordinates[:,atom_indices,:]
            tmp_item.coordinates = tmp_item.coordinates[frame_indices,:,:]
            tmp_item.box_shape = deepcopy(self.box_shape)

            tmp_item.atom_indices = atom_indices
            tmp_item.n_frames = len(frame_indices)
            tmp_item.n_atoms = len(atom_indices)

            tmp_item.file = item.file.duplicate()

        return tmp_item

    def duplicate (self):

        from copy import deepcopy

        tmp_item = Trajectory()

        tmp_item.length_units = deepcopy(self.length_units)
        tmp_item.time_units = deepcopy(self.time_units)

        tmp_item.step = deepcopy(self.step)
        tmp_item.time = deepcopy(self.time)
        tmp_item.coordinates = deepcopy(self.coordinates)
        tmp_item.box = deepcopy(self.box)
        tmp_item.box_shape = deepcopy(self.box_shape)

        tmp_item.atom_indices = deepcopy(self.atom_indices)
        tmp_item.n_frames = deepcopy(self.n_frames)
        tmp_item.n_atoms = deepcopy(self.n_atoms)

        tmp_item.file = self.file.duplicate()

        return tmp_item


    #def cell2box(self):
    #    self.box,self.volume,self.orthogonal=_libbox.cell2box(self.cell, self.n_frames)
    #    pass

    #def box2cell(self):
    #    self.cell,self.volume,self.orthogonal=_libbox.box2cell(self.box, self.n_frames)
    #    pass

    #def box2invbox(self):
    #    self.invbox=_libbox.box2invbox(self.box, self.n_frames)
    #    pass

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

