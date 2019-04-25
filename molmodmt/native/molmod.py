from .trajectory import Trajectory as _Trajectory

class MolMod():

    def __init__(self):

        self.trajectory = None
        self.structure = None
        self.topology = None
        self.topography = None

    def extract(self, atoms_list=None):

        from molmodmt import extract as _extract
        from molmodmt import get_form as _get_form

        tmp_item = MolMod()
        tmp_item.topology = _extract(self.topology,selection=atoms_list)
        tmp_item.trajectory = _extract(self.trajectory,selection=atoms_list)
        tmp_item.topography = None
        tmp_item.structure = None

        return tmp_item

    def select_with_mdtraj(self, selection=None):
        return self.topology.select(selection)

