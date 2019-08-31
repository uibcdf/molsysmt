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

        self.length_units = None
        self.time_units = None

        self.step  = None
        self.time  = None
        self.coordinates = None # ndarray with shape=(n_frames, n_atoms, 3) and dtype=float
                                # and order=F, with units nanometers
        self.cell  = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'

        self.orthogonal   = None # True or False
        self.n_frames = 0
        self.n_atoms = 0

        from .trajectory_file import TrajectoryFile
        self.file = TrajectoryFile(filename=filename)

    def _set_frames(self, step=None, time=None, coordinates=None, cell=None):

        self.coordinates = coordinates
        self.time  = time
        self.step  = step
        self.box   = box
        self.cell  = cell
        self.delta_time  = delta_time
        self.delta_steps  = delta_steps

        if box is not None:
            if box[0] is None:
                self.box = None

        if cell is not None:
            if cell[0] is None:
                self.cell = None

        if self.coordinates is not None:
            self.n_frames = self.coordinates.shape[0]
            self.n_atoms = self.coordinates.shape[1]

        if self.n_frames > 1:
            if self.delta_time is None and self.time is not None:
                self.delta_time=_np.mean(self.time[1:]-self.time[:-1])
            if self.delta_steps is None and self.step is not None:
                self.delta_steps=_np.mean(self.step[1:]-self.step[:-1])

        ii = self.coordinates
        if ii is not None:
            if _np.isfortran(ii)==False:
                ii=_np.asfortranarray(ii)

        ii = self.box
        if ii is not None:
            if _np.isfortran(ii)==False:
                ii=_np.asfortranarray(ii)

        ii = self.cell
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

        if (self.cell is None) and (self.box is not None):
            self.box2cell()

        if (self.cell is not None) and (self.box is None):
            self.cell2box()

        if (self.box is not None):
            self.box2invbox()

        pass

    def cell2box(self):
        self.box,self.volume,self.orthogonal=_libbox.cell2box(self.cell, self.n_frames)
        pass

    def box2cell(self):
        self.cell,self.volume,self.orthogonal=_libbox.box2cell(self.box, self.n_frames)
        pass

    def box2invbox(self):
        self.invbox=_libbox.box2invbox(self.box, self.n_frames)
        pass

    #def extract(self, atom_indices=None):

    #    tmp_item=deepcopy(self)
    #    tmp_item.coordinates=tmp_item.coordinates[:,atom_indices,:]
    #    tmp_item.n_atoms=len(atom_indices)

    #    return tmp_item

    def get_cell_lengths(self):

        return self.cell[:,[0,1,2],[0,1,2]]

    def get_cell_angles(self):

        return self.cell[:,[0,0,1],[1,2,2]]

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

    def load_frames (self, frame_indices=None, atom_indices=None):

        from molmodmt import get

        if atom_indices == 'all':
            atom_indices = self.atom_indices

        coordinates, time, step, box = get(self.file.mount_point, element='atom',
                indices=atom_indices, frame_indices=frame_indices, frames=True)

        self._set_frames(coordinates, time, step, box)
        self.file.atom_indices = atom_indices
        del(coordinates, time, step, box)

        pass

