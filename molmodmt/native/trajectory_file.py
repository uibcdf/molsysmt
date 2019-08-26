class TrajectoryFile():

    def __init__(self, filename=None, mode='read'):

        self.opened = False
        self.filename = None
        self.mount_point = None
        self.form = None
        self.n_frames = 0

        if filename is not None and mode=='read':

            from molmodmt import get, get_form, convert

            self.filename = filename
            self.form = get_form(filename)

            if self.form == 'xtc':
                self.mount_point = convert(filename,'mdtraj.XTCTrajectoryFile')
                self.n_frames = get(self.mount_point, n_frames=True)
                self.opened = True
            else:
                raise NotImplementedError

    def load_frames (self, indices=None, atoms_indices=None):

        from molmodmt import get
        return get(self.mount_point, indices=atoms_indices, frame_indices=indices)
