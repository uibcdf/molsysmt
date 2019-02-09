import numpy as _np
from simtk import unit as _unit
#import lib.libcell2box as libbox
#from .lib import libframe as libbox
from copy import deepcopy

# Tiene que haber una manera automatica con f2py dar siempre de salida Ccontiguous_np.arrays

class Trajectory():

    def __init__(self,coordinates=None, box=None, cell=None, timestep=None, integstep=None,
                 steps=None, times=None):

        self.__name__="patata"

        self.coordinates = None
        self.box   = None #_np.zeros(shape=(3,3),dtype=float,order='F')
        self.timestep  = None
        self.integstep  = None
        self.steps  = None
        self.times  = None
        self.model = None # In case it is a model and not a timestep

        self.invbox       = None #_np.zeros(shape=(3,3),dtype=float,order='F')
        self.cell         = None #_np.zeros(shape=(3,3),dtype=float,order='F')
        self.orthogonal   = 0
        self.volume       = 0.0

        self._length_units = _unit.nanometers
        self._time_units     = _unit.picoseconds

        self.coordinates = coordinates
        self.box   = box
        self.cell  = cell
        self.timestep  = timestep
        self.integstep  = integstep
        self.steps  = steps
        self.times  = times


    def Cell2Box(self):
        #self.box,self.volume,self.orthogonal=libbox.cell2box(asfortran_np.array(self.cell))
        #self.box=ascontiguous_np.array(self.box)
        pass

    def Box2Cell(self):
        #self.cell,self.volume,self.orthogonal=libbox.box2cell(asfortran_np.array(self.box))
        #self.cell=ascontiguous_np.array(self.cell)
        pass

    def Box2Invbox(self):
        #self.invbox=libbox.box2invbox(self.box)
        #self.invbox=ascontiguous_np.array(self.invbox)
        pass

    def Unwrap(self,selection=None,min_image_selection=None):

        #self.frame=ascontiguous_np.array(Tools.Unwrap()) 
        pass

    def Wrap(self):

        #self.coors=asfortran_np.array(self.coors)
        #libbox.wrap_all_inplace(self.coors,self.box,self.invbox,self.orthogonal,self.coors.shape[0])
        #self.coors=ascontiguous_np.array(self.coors)
        pass

    def LoadBox(self,box=None,wrap=False):

        #self.box=box
        #self.Box2Cell()
        #self.Box2Invbox()
        #if wrap:
        #    self.Wrap()
        pass

    def Fix(self,wrap=True):

        #if self.cell is None:
        #    self.Box2Cell()
        #elif self.box is None:
        #    self.Cell2Box()
        #if self.invbox is None:
        #    self.Box2Invbox()
        #if wrap:
        #    self.Wrap()
        pass

    def Extract(self,selection=None):  # Extract new frame complete frame from selection

        #tmp_frame=deepcopy(self)
        #tmp_frame.coors=tmp_frame.coors[selection,:]

        #return tmp_frame
        pass
