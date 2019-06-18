class MolMod():

    def __init__(self):

        self.trajectory = None
        self.structure = None
        self.topology = None
        self.topography = None

    def extract(self, atom_indices=None):

        from molmodmt import extract as _extract
        from molmodmt import get_form as _get_form

        tmp_item = MolMod()
        tmp_item.topology = _extract(self.topology,selection=atom_indices)
        tmp_item.trajectory = _extract(self.trajectory,selection=atom_indices)
        tmp_item.topography = None
        tmp_item.structure = None

        return tmp_item

    def select(self, selection=None, syntaxis='mdtraj'):
        if syntaxis=='mdtraj':
            return self._select_with_mdtraj(selection=selection)
        else:
            raise NotImplementedError

    def _select_with_mdtraj(self, selection=None):
        return self.topology.select(selection)

