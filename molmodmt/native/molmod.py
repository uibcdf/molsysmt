class MolMod():

    def __init__(self):

        self.trajectory = None
        self.structure = None
        self.topology = None
        self.topography = None

    def extract(self, atom_indices=None, mode='keeping_selection'):

        from molmodmt import extract as _extract

        tmp_item = MolMod()
        tmp_item.topology = _extract(self.topology, selection=atom_indices, mode=mode)
        tmp_item.trajectory = _extract(self.trajectory, selection=atom_indices, mode=mode)
        tmp_item.topography = None
        tmp_item.structure = None

        return tmp_item

    def select(self, selection=None, syntaxis='MDTraj'):
        from molmodmt import select as _select
        return _select(self.topology, selection=selection, syntaxis=syntaxis)

    def load_frames(self, frame_indices=None, selection=None, syntaxis='MDTraj'):
        atom_indices = self.select(selection=selection, syntaxis=syntaxis)
        return self.trajectory.load_frames(frame_indices=frame_indices, atom_indices=atom_indices)

