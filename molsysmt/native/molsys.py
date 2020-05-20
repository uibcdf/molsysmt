class MolSys():

    def __init__(self):

        self.topology = None
        self.trajectory = None

    def extract(self, atom_indices='all', frame_indices='all'):

        from molsysmt.utils.frame_indices import digest as digest_frame_indices

        if (atom_indices is 'all') and (frame_indices is 'all'):

            return self.copy()

        else:

            frame_indices = digest_frame_indices(self, frame_indices)
            tmp_item = MolSys()
            tmp_item.topology = self.topology.extract(atom_indices=atom_indices, frame_indices=frame_indices)
            tmp_item.trajectory = self.trajectory.extract(atom_indices=atom_indices, frame_indices=frame_indices)

            return tmp_item

    def load_frames(self, selection='all', frame_indices='all', syntaxis='MDTraj'):

        atom_indices = self.select(selection=selection, syntaxis=syntaxis)
        return self.trajectory.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)

    def copy(self):

        tmp_item = MolSys()
        tmp_item.trajectory = self.trajectory.copy()
        tmp_item.topology = self.topology.copy()

        return tmp_item

