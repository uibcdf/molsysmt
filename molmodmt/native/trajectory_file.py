class TrajectoryFile():

    def __init__(self, filename=None, mode='read'):

        self.opened = False
        self.name = None
        self.mount_point = None
        self.form = None
        self.n_frames = 0
        self.n_atoms = 0
        self.box_shape = None
        self.atom_indices = None

        if filename is not None and mode=='read':

            from molmodmt import get, get_form, convert

            self.name = filename
            self.form = get_form(filename)

            if self.form == 'xtc':
                self.mount_point = convert(filename,'mdtraj.XTCTrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.n_atoms = get(self.mount_point, n_atoms=True)
                self.box_shape = get(self.mount_point, box_shape=True)
                self.opened = True
            elif self.form == 'h5':
                self.mount_point = convert(filename,'mdtraj.HDF5TrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.n_atoms = get(self.mount_point, n_atoms=True)
                self.box_shape = get(self.mount_point, box_shape=True)
                self.opened = True
            elif self.form == 'pdb':
                self.mount_point = convert(filename,'mdtraj.PDBTrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.n_atoms = get(self.mount_point, n_atoms=True)
                self.box_shape = get(self.mount_point, box_shape=True)
                self.opened = True
            else:
                raise NotImplementedError

    def load_frames (self, indices=None, atoms_indices=None):

        # return: step, time, coordinates, box   (with units)

        from molmodmt import get
        return get(self.mount_point, indices=atoms_indices, frame_indices=indices)

