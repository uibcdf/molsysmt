import numpy as np

# Ver: https://anaconda.org/conda-forge/xdrfile
# Ver: https://bmcresnotes.biomedcentral.com/articles/10.1186/s13104-021-05536-5
# Ver: https://github.com/gromacs/gromacs

class XTCFile():

    def __init__(self, filename=None, mode='read'):

        self.opened = False
        self.filename = None
        self.mount_point = None
        self.mode = None
        self.atom_indices = None
        self.io_position = None
        self.io_error=False

        self.n_atoms = None
        self.n_structures = None
        self.pos_header = None
        self.pos_frame = None
        self.box_initial_frame = None


