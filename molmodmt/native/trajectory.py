import numpy as _np
from simtk import unit as _unit
from molmodmt.lib import box as _libbox
from molmodmt.utils.exceptions import *
from copy import deepcopy

# Tiene que haber una manera automatica con f2py dar siempre de salida Ccontiguous_np.arrays

class Trajectory():

    def __init__(self, filename=None):

        self.filename = None
        self.coordinates = None # ndarray with shape=(n_frames, n_atoms, 3) and dtype=float
                                # and order=F, with units nanometers
        self.box   = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'
        self.cell  = None # ndarray with shape=(n_frames,3,3), dtype=float and order='F'
        self.timestep  = None
        self.integstep  = None
        self.step  = None
        self.time  = None
        self.model = None # In case it is a model and not a timestep

        self.invbox       = None #_np.zeros(shape=(n_frames,3,3),dtype=float,order='F')
        self.orthogonal   = 0
        self.volume       = 0.0

        self.topology = None
        self.topology_mdtraj= None
        self.topography = None
        self.structure = None

        self._length_units = _unit.nanometers
        self._time_units     = _unit.picoseconds

        self.filename = filename

    def _import_mdtraj_data(self,item=None):

        from .io_trajectory import parse_mdtraj_Trajectory
        tmp_coordinates, tmp_box, tmp_time, tmp_timestep = parse_mdtraj_Trajectory(item)
        self._initialize_with_coors(coordinates=tmp_coordinates, box=tmp_box, timestep=tmp_timestep,
                                    time=tmp_time)
        pass

    def _initialize_with_coors(self, coordinates=None, box=None, cell=None, timestep=None, integstep=None,
                 step=None, time=None):

        self.coordinates = coordinates
        self.box   = box
        self.cell  = cell
        self.timestep  = timestep
        self.integstep  = integstep
        self.step  = step
        self.time  = time

        if self.coordinates is not None:
            self.nframes = self.coordinates.shape[0]
            self.natoms = self.coordinates.shape[1]

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
        self.box,self.volume,self.orthogonal=_libbox.cell2box(self.cell, self.nframes)
        pass

    def box2cell(self):
        self.cell,self.volume,self.orthogonal=_libbox.box2cell(self.box, self.nframes)
        pass

    def box2invbox(self):
        self.invbox=_libbox.box2invbox(self.box, self.nframes)
        pass

    def unwrap(self,selection=None,min_image_selection=None):
        #self.frame=ascontiguous_np.array(Tools.Unwrap()) 
        pass

    def wrap(self):
        #self.coors=asfortran_np.array(self.coors)
        #libbox.wrap_all_inplace(self.coors,self.box,self.invbox,self.orthogonal,self.coors.shape[0])
        #self.coors=ascontiguous_np.array(self.coors)
        pass

    def extract(self,selection=None):  # Extract new frame complete frame from selection
        #tmp_frame=deepcopy(self)
        #tmp_frame.coors=tmp_frame.coors[selection,:]
        #return tmp_frame
        pass

    def iterload(self,chunk=100, stride=1, skip=0, selection=None):

        from mdtraj import iterload as _mdtraj_iterload
        tmp_top = self.topology_mdtraj

        iterator = _mdtraj_iterload(self.filename, top=tmp_top, chunk=chunk,
                                                stride=stride, atom_indices=None)

        while True:
            tmp_mdtraj = next(iterator)
            if tmp_mdtraj is None:
                return
            self._import_mdtraj_data(tmp_mdtraj)
            del(tmp_mdtraj)
            yield

    def load(self,frame=None):

        from mdtraj import load as _mdtraj_load
        from mdtraj import load_frame as _mdtraj_load_frame
        from .io_topology import to_mdtraj_Topology as _to_mdtraj_Topology
        from numpy import ndarray

        tmp_top = self.topology_mdtraj
        mdtraj_read = False

        if type(frame)==str:
            if frame.lower()=='all':
                tmp_mdtrajectory = _mdtraj_load(self.filename,top=tmp_top)
                mdtraj_read = True
        elif type(frame)==int:
            tmp_mdtrajectory = _mdtraj_load_frame(self.filename,frame,top=tmp_top)
            mdtraj_read = True
        elif type(frame) in [list,tuple,ndarray]:
            tmp_mdtrajectory = _mdtraj_load_frame(self.filename,frame[0],top=tmp_top)
            mdtraj_read = True
            for ii in range(1,len(frame)):
                tmp_mdtrajectory.join(_mdtraj_load_frame(self.filename,frame[ii],top=tmp_top),check_topology=False)

        if mdtraj_read:
            self._import_mdtraj_data(tmp_mdtrajectory)
        else:
            raise BadCallError(BadCallMessage)

