class TrajectoryFile():

    def __init__(self, file_path=None, mode='read'):

        self.opened = False
        self.path = None
        self.mount_point = None
        self.form = None
        self.n_frames = 0
        self.n_atoms = 0
        self.atom_indices = None

        if file_path is not None and mode=='read':

            from molsysmt.multitool import _get_form
            from molsysmt import get, convert

            self.path = file_path
            self.form = _get_form(file_path)

            if self.form == 'xtc':
                self.mount_point = convert(file_path, to_form='mdtraj.XTCTrajectoryFile')
            elif self.form == 'h5':
                self.mount_point = convert(file_path, to_form='mdtraj.HDF5TrajectoryFile')
            elif self.form == 'pdb':
                self.mount_point = convert(file_path, to_form='mdtraj.PDBTrajectoryFile')
            elif self.form == 'mmtf':
                self.mount_point = convert(file_path, to_form='mmtf.MMTFDecoder')
            else:
                raise NotImplementedError

            self.n_frames = get(self.mount_point, target='system', n_frames=True)
            self.n_atoms = get(self.mount_point, target='system', n_atoms=True)
            self.opened = True

    def read_frames (self, atom_indices='all', frame_indices='all'):

        from molsysmt import get
        step, time, coordinates, box = get(self.mount_point, target='atom', indices=atom_indices, frame_indices=frame_indices, frames=True)
        self.atom_indices=atom_indices
        return step, time, coordinates, box

    def duplicate (self):

        from copy import deepcopy
        tmp_item = TrajectoryFile(filename=self.name, mode='read')
        tmp_item.atom_indices = deepcopy(item.atom_indices)
        return tmp_item

