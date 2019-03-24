from .trajectory import Trajectory as _Trajectory


class MolMod():

    def __init__(self):

        self.trajectory = _Trajectory()
        self.structure = None
        self.topology = None
        self.topography = None

    def extract(self, atoms_list=None):

        tmp_MolMod = MolMod()
        tmp.structure = self.topology.extract(atoms_list)
        tmp.topology = self.topology.extract(atoms_list)
        tmp.topography = None
        tmp.trajectory = self.trajectory.extract(atoms_list)

        return tmp_MolMod

    def select_with_mdtraj(self, selection=None):
        return self.trajectory.topology_mdtraj.select(selection)

