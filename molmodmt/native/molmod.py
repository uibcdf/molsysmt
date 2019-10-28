class MolMod():

    def __init__(self):

        self.trajectory = None
        self.structure = None
        self.topology = None
        self.topography = None

    def extract(self, atom_indices='all', frame_indices='all'):

        from .molmodmt.forms.classes.api_molmodmt_Topology import extract_subsystem as extract_topology
        from .molmodmt.forms.classes.api_molmodmt_Trajectory import extract_subsystem as extract_trajectory

        tmp_item = MolMod()
        tmp_item.topology = extract_topology(self.topology, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item.trajectory = extract_trajectory(self.trajectory, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item.topography = None
        tmp_item.structure = None

        return tmp_item

    def select(self, selection=None, syntaxis='MDTraj'):
        from molmodmt import select as _select
        return _select(self.topology, selection=selection, syntaxis=syntaxis)

    def load_frames(self, frame_indices='all', selection='all', syntaxis='MDTraj'):
        atom_indices = self.select(selection=selection, syntaxis=syntaxis)
        return self.trajectory.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)

