class MolSys():

    def __init__(self):

        from .topology import Topology
        from .trajectory import Trajectory

        self.topology = Topology()
        self.trajectory = Trajectory()

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

    def add(self, item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

        from molsysmt import convert, get_form, select

        if get_form(item)!='molsysmt.MolSys':
            tmp_item = convert(item, selection=atom_indices, frame_indices=frame_indices, to_form='molsysmt.MolSys')
            self.topology.add(tmp_item.topology)
            self.trajectory.add(tmp_item.trajectory)
        else:
            atom_indices=select(item, selection=selection, syntaxis=syntaxis)
            self.topology.add(item.topology, selection=atom_indices)
            self.trajectory.add(item.trajectory, selection=atom_indices,frame_indices=frame_indices)

    def load_frames(self, selection='all', frame_indices='all', syntaxis='MoolSysMT'):

        atom_indices = self.select(selection=selection, syntaxis=syntaxis)
        return self.trajectory.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)

    def copy(self):

        tmp_item = MolSys()
        tmp_item.trajectory = self.trajectory.copy()
        tmp_item.topology = self.topology.copy()

        return tmp_item

