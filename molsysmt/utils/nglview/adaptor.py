## This should go here: nglview/nglview/adaptor.py

import os
import warnings
import os.path
import uuid
from functools import partial
from io import StringIO
from tempfile import NamedTemporaryFile
from urllib.request import urlopen

import numpy as np

from nglview import config
from nglview.base_adaptor import Structure, Trajectory
from nglview.utils.py_utils import FileManager, tempfolder

def _get_structure_string(write_method, suffix='.pdb'):
    with NamedTemporaryFile(suffix=suffix) as fh:
        write_method(fh.name)
        return fh.read().decode()


class register_backend:
    def __init__(self, package_name):
        # package_name must match exactly to your Python package
        self.package_name = package_name

    def __call__(self, cls):
        config.BACKENDS[self.package_name] = cls
        return cls


@register_backend('molsysmt')
class MolSysMTTrajectory(Trajectory, Structure):
    '''MolSysMT adaptor.

    Visit [MolSysmt documentation webpage](xxx) for further info.

    Example
    -------
    >>> import nglview as nv
    >>> import molsysmt as msm
    >>> traj = msm.convert([nv.datafiles.GRO, nv.datafiles.XTC], to_form='molsysmt.MolSys')
    >>> t = nv.MolSysMTTrajectory(traj)
    >>> w = nv.NGLWidget(t)
    >>> w
    '''

    def __init__(self, molsys, atom_indices='all', frame_indices='all'):
        self.dataframe = molsys.topology.dataframe.extract(atom_indices)
        self.trajectory = molsys.trajectory.extract(atom_indices, frame_indices)
        self.ext = "pdb"
        self.params = {}
        self.id = str(uuid.uuid4())

    def get_coordinates(self, index):
            return 10.0*self.trajectory.coordinates[index]._value

    @property
    def n_frames(self):
        return self.trajectory.n_frames

    def get_structure_string(self):

        return self.dataframe._to_pdb(self.trajectory, frame_indices=0)

