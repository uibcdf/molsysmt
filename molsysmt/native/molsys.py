class MolSys():

    def __init__(self):

        self.trajectory = None
        self.topology = None
        self.composition = None
        self.topography = None
        self.structure_obtention = None
        self.card = None

    def extract(self, selection='all', frame_indices='all', syntaxis='MDTraj'):

        from molsysmt.utils.atom_indices import digest as digest_atom_indices
        from molsysmt.utils.frame_indices import digest as digest_frame_indices

        if (selection is 'all') and (frame_indices is 'all'):

            return self

        else:

            atom_indices = self.select(selection=selection, syntaxis=syntaxis)
            frame_indices = digest_frame_indices(frame_indices)

            from .molsysmt.forms.classes.api_mdtraj_Topology import extract_subsystem as extract_mdtraj_Topology

            tmp_item = MolSys()
            tmp_item.topology = extract_topology(self.topology, atom_indices=atom_indices, frame_indices=frame_indices)
            tmp_item.trajectory = self.trajectory.extract(atom_indices=atom_indices, frame_indices=frame_indices)
            tmp_item.topography = self.extract(atom_indices=atom_indices, frame_indices=frame_indices)
            self.structure_obtention = self.structure_obtention.extract(atom_indices=atom_indices, frame_indices=frame_indices)
            self.card = self.card.extract(atom_indices=atom_indices, frame_indices=frame_indices)

            return tmp_item

    def select(self, selection=None, syntaxis='MDTraj'):

        from molsysmt import select as _select
        return _select(self.topology, selection=selection, syntaxis=syntaxis)

    def load_frames(self, selection='all', frame_indices='all', syntaxis='MDTraj'):

        atom_indices = self.select(selection=selection, syntaxis=syntaxis)
        return self.trajectory.load_frames(atom_indices=atom_indices, frame_indices=frame_indices)

    def duplicate(self):

        tmp_item = MolSys()
        tmp_item.trajectory = self.trajectory.duplicate()
        tmp_item.topology = self.topology.copy()
        tmp_item.composition = self.composition.duplicate()
        tmp_item.topography = self.topography.duplicate()
        tmp_item.structure_obtention = self.structure_obtention.duplicate()

        return tmp_item

