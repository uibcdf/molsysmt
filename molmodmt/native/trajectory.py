import numpy as _np
from simtk import unit as _unit
from molmodmt.lib import box as _libbox
from copy import deepcopy

# Tiene que haber una manera automatica con f2py dar siempre de salida Ccontiguous_np.arrays

class Trajectory():

    def __init__(self, filename=None, coordinates=None, box=None, cell=None, timestep=None, integstep=None,
                 step=None, time=None):

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

        self._length_units = _unit.nanometers
        self._time_units     = _unit.picoseconds

        self.filename = filename
        self.coordinates = coordinates
        self.box   = box
        self.cell  = cell
        self.timestep  = timestep
        self.integstep  = integstep
        self.steps  = step
        self.times  = time

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
            self.Box2Cell()

        if (self.cell is not None) and (self.box is None):
            self.Cell2Box()

        if (self.box is not None):
            self.Box2Invbox()

    def Cell2Box(self):
        self.box,self.volume,self.orthogonal=_libbox.cell2box(self.cell, self.nframes)
        pass

    def Box2Cell(self):
        self.cell,self.volume,self.orthogonal=_libbox.box2cell(self.box, self.nframes)
        pass

    def Box2Invbox(self):
        self.invbox=_libbox.box2invbox(self.box, self.nframes)
        pass

    def Unwrap(self,selection=None,min_image_selection=None):
        #self.frame=ascontiguous_np.array(Tools.Unwrap()) 
        pass

    def Wrap(self):
        #self.coors=asfortran_np.array(self.coors)
        #libbox.wrap_all_inplace(self.coors,self.box,self.invbox,self.orthogonal,self.coors.shape[0])
        #self.coors=ascontiguous_np.array(self.coors)
        pass

    def Extract(self,selection=None):  # Extract new frame complete frame from selection
        #tmp_frame=deepcopy(self)
        #tmp_frame.coors=tmp_frame.coors[selection,:]
        #return tmp_frame
        pass

