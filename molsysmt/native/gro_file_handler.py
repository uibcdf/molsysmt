import numpy as np
from molsysmt import pyunitwizard as puw
import io
from pathlib import PosixPath


class GROAtomicCoordinateEntry():

    def __init__(self):

        self.header = None
        self.n_atoms = 0
        self.atom_names = None
        self.atom_ids = None
        self.atom_group_index = None
        self.n_groups = 0
        self.group_names = None
        self.group_ids = None
        self.coordinates = None
        self.velocities = None
        self.box = None


def parse(file):

    gro = GROAtomicCoordinateEntry()

    gro.header = file.readline().strip()    
    gro.n_atoms = int(file.readline().strip())

    gro.atom_names = np.ndarray(shape=[gro.n_atoms], dtype=object)
    gro.atom_ids = np.ndarray(shape=[gro.n_atoms], dtype=int)
    gro.atom_group_index = np.ndarray(shape=[gro.n_atoms], dtype=int)
    gro.group_names = []
    gro.group_ids = []
    gro.coordinates = np.ndarray(shape=[gro.n_atoms,3], dtype=float)
    gro.velocities = None
    gro.box = np.zeros([3,3], dtype=float)

    group_index = -1
    former_group_id = -1
    check_velocities = True
    with_velocities = False
        
    for ii in range(gro.n_atoms):

        line = file.readline()
    
        group_id = int(line[:5])

        if former_group_id!=group_id:
            gro.group_ids.append(group_id)
            gro.group_names.append(line[5:10].strip())
            group_index+=1
            former_group_id=group_id
    
        gro.atom_ids[ii]=int(line[15:20])
        gro.atom_names[ii]=line[10:15].strip()
        gro.atom_group_index[ii]=group_index

        gro.coordinates[ii,:]=[float(line[20:28]), float(line[28:36]), float(line[36:44])]
    
        if check_velocities:
            if len(line)>68:
                gro.velocities = np.ndarray(shape=[gro.n_atoms,3], dtype=float)
                with_velocities = True
                check_velocities = False
    
        if with_velocities:
            gro.velocities[ii,:]=[float(line[44:52]), float(line[52:60]), float(line[60:68])]

    box_values = file.readline().split()
    
    gro.box[0,0] = float(box_values[0])
    gro.box[1,1] = float(box_values[1])
    gro.box[2,2] = float(box_values[2])
    
    if len(box_values)==9:
        gro.box[0,1] = float(box_values[3])
        gro.box[0,2] = float(box_values[4])
        gro.box[1,0] = float(box_values[5])
        gro.box[1,2] = float(box_values[6])
        gro.box[2,0] = float(box_values[7])
        gro.box[2,1] = float(box_values[8])

    gro.coordinates=puw.quantity(gro.coordinates,'nm')
    gro.box=puw.quantity(gro.box,'nm')
    if with_velocities:
        gro.velocities=puw.quantity(gro.velocities,'nm/ps')

    gro.group_ids = np.array(gro.group_ids, dtype=int)
    gro.group_names = np.array(gro.group_names, dtype=object)
    gro.n_groups = gro.group_ids.shape[0]

    return gro

class GROFileHandler():

    def __init__(self, file, io_mode='r', closed=False, skip_digestion=False):


        self.file = None
        self.entry = None

        if isinstance(file, PosixPath):
            file = str(file)

        if isinstance(file, str):

            if file.endswith('.gro'):

                if io_mode=='w':

                    self.file = None

                elif io_mode=='r':

                    self.file = open(file, "r")
                    self.load()

                else:

                    raise NotImplementedError

            else:


                if io_mode=='r':
                    file = io.StringIO(file)

        if isinstance(file, io.StringIO):
            if io_mode=='r':
                self.file = file
                self.load()

        if closed:
            self.file.close()

    def close(self):

        self.file.close()

    def load(self):

        self.entry = parse(self.file)

    def dump(self):

        pass

