import numpy as _np
from simtk import unit as _unit
from molmodmt.lib import box as _libbox
from molmodmt.lib import com as _libcom
from molmodmt.utils.exceptions import *
from copy import deepcopy

# Tiene que haber una manera automatica con f2py dar siempre de salida Ccontiguous_np.arrays

class Trajectory():

    def __init__(self, filename=None):

        self._filename = filename
        self._file = None

        self.coordinates = None # ndarray with shape=(n_frames, n_atoms, 3) and dtype=float
                                # and order=F, with units nanometers
        self.box   = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'
        self.cell  = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'
        self.timestep  = None
        self.integstep = None
        self.step  = None
        self.time  = None
        self.model = None # In case it is a model and not a timestep
        self.n_frames = 0
        self.n_atoms = 0

        self.invbox       = None #_np.zeros(shape=(n_frames,3,3),dtype=float,order='F')
        self.orthogonal   = 0
        self.volume       = 0.0

        self._length_units = _unit.nanometers
        self._time_units = _unit.picoseconds

    def _initialize_with_attributes(self, coordinates=None, box=None, cell=None, timestep=None,
                                    integstep=None, step=None, time=None):

        self.coordinates = coordinates
        self.box   = box
        self.cell  = cell
        self.timestep  = timestep
        self.integstep  = integstep
        self.step  = step
        self.time  = time

        if box is not None:
            if box[0] is None:
                self.box = None

        if cell is not None:
            if cell[0] is None:
                self.cell = None

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

    def extract(self, atom_indices=None):

        tmp_item=deepcopy(self)
        tmp_item.coordinates=tmp_item.coordinates[:,atom_indices,:]
        tmp_item.n_atoms=len(atom_indices)

        return tmp_item

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

    def load(self, frame_indices='all', atom_indices='all'):

        pass

    #def load(self, frame_indices='all', atom_indices='all'):

    #    from mdtraj import load as _mdtraj_load
    #    from mdtraj import join as _mdtraj_join
    #    from mdtraj import load_frame as _mdtraj_load_frame
    #    from .io_topology import to_mdtraj_Topology as _to_mdtraj_Topology
    #    from numpy import ndarray

    #    tmp_top = self.topology_mdtraj
    #    mdtraj_read = False
    #    atom_indices = None

    #    if selection is None:
    #        if self.selection_mdtraj is not None:
    #            atom_indices = self._atom_indices_mdtraj
    #    else:
    #        from molmodmt.multitool import select as _select
    #        atom_indices = _select(self.topology_mdtraj,selection,syntaxis)

    #    if type(frame_indices)==str:
    #        if frame.lower()=='all':
    #            tmp_mdtrajectory = _mdtraj_load(self.filename,top=tmp_top,atom_indices=atom_indices)
    #            mdtraj_read = True
    #    elif type(frame_indices)==int:
    #        tmp_mdtrajectory = _mdtraj_load_frame(self.filename,frame_indices,top=tmp_top,atom_indices=atom_indices)
    #        mdtraj_read = True
    #    elif type(frame_indices) in [list,tuple,ndarray]:
    #        mdtraj_read = True
    #        tmp_trajs=[]
    #        for ii in range(0,len(frame_indices)):
    #            tmp_trajs.append(_mdtraj_load_frame(self.filename, frame_indices[ii],top=tmp_top, atom_indices=atom_indices))
    #        tmp_mdtrajectory=_mdtraj_join(tmp_trajs,check_topology=False)
    #        del(tmp_trajs)

    #    if mdtraj_read:
    #        self._import_mdtraj_data(tmp_mdtrajectory)
    #        if atom_indices is not None:
    #            self._import_mdtraj_topology(tmp_mdtrajectory)
    #    else:
    #        raise BadCallError(BadCallMessage)



