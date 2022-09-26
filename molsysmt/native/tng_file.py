import numpy as np

# Ver: https://onlinelibrary.wiley.com/doi/10.1002/jcc.23495
# Ver: https://github.com/gromacs/tng


class TNGFile():

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



