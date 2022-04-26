class TrajectoryFile():

    def __init__(self, filepath=None, mode='read'):

        self.opened = False
        self.path = None
        self.mount_point = None
        self.form = None
        self.n_structures = 0
        self.n_atoms = 0
        self.atom_indices = None

        if filepath is not None and mode=='read':

            from molsysmt.basic import get_form
            from molsysmt import get, convert

            self.path = filepath
            self.form = get_form(filepath)

            if self.form == 'file:xtc':
                self.mount_point = convert(filepath, to_form='mdtraj.XTCTrajectoryFile')
            elif self.form == 'file:h5':
                self.mount_point = convert(filepath, to_form='mdtraj.HDF5TrajectoryFile')
            elif self.form == 'file:pdb':
                # Don't use mdtraj.PDBTrajectoryFile. It does not work well with alternate
                # locations in a pdb
                self.mount_point = convert(filepath, to_form='openmm.PDBFile')
            elif self.form == 'file:inpcrd':
                self.mount_point = convert(filepath, to_form='mdtraj.AmberRestartFile')
            elif self.form == 'file:mmtf':
                self.mount_point = convert(filepath, to_form='mmtf.MMTFDecoder')
            elif self.form == 'file:gro':
                self.mount_point = convert(filepath, to_form='openmm.GromacsGroFile')
            else:
                raise NotImplementedError

            self.n_structures = get(self.mount_point, target='system', n_structures=True)
            self.n_atoms = get(self.mount_point, target='system', n_atoms=True)
            self.opened = True

    def read_frames(self, atom_indices='all', structure_indices='all'):

        from molsysmt import get
        from molsysmt.basic import get_form
        step, time, coordinates, box = get(self.mount_point, target='atom', indices=atom_indices, structure_indices=structure_indices, frame=True)
        self.atom_indices=atom_indices
        return step, time, coordinates, box

    def copy(self):

        tmp_item = TrajectoryFile()
        return tmp_item

