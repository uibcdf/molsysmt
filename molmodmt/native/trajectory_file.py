class TrajectoryFile():

    def __init__(self, file_path=None, mode='read'):

        self.opened = False
        self.path = None
        self.mount_point = None
        self.form = None
        self.n_frames = 0
        self.n_atoms = 0
        self.box_shape = None
        self.atom_indices = None

        if file_path is not None and mode=='read':

            from molmodmt import get, get_form, convert

            self.path = file_path
            self.form = get_form(file_path)

            if self.form == 'xtc':
                self.mount_point = convert(file_path, to_form='mdtraj.XTCTrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.n_atoms = get(self.mount_point, n_atoms=True)
                self.box_shape = get(self.mount_point, box_shape=True)
                self.opened = True
            elif self.form == 'h5':
                self.mount_point = convert(file_path, to_form='mdtraj.HDF5TrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.n_atoms = get(self.mount_point, n_atoms=True)
                self.box_shape = get(self.mount_point, box_shape=True)
                self.opened = True
            elif self.form == 'pdb':
                self.mount_point = convert(file_path, to_form='mdtraj.PDBTrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.n_atoms = get(self.mount_point, n_atoms=True)
                self.box_shape = get(self.mount_point, box_shape=True)
                self.opened = True
            else:
                raise NotImplementedError

    def load_frames (self, atom_indices=None, frame_indices=None):

        # return: step, time, coordinates, box   (with units)

        from molmodmt import get
        step, time, coordinates, box = get(self.mount_point, target='atom', indices=atom_indices,
                                       frame_indices=frame_indices, frames=True)
        self.atom_indices=atom_indices
        return step, time, coordinates, box

