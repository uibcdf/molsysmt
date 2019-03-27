from .trajectory import Trajectory as _Trajectory

class MolMod():

    def __init__(self):

        self.trajectory = _Trajectory()
        self.structure = None
        self.topology = None
        self.topography = None

    def extract(self, atoms_list=None):

        from molmodmt import extract as _extract

        tmp_MolMod = MolMod()
        tmp_MolMod.structure = _extract(self.structure, atoms_list)
        tmp_MolMod.topology = tmp_MolMod.structure.topology
        tmp_MolMod.topography = None
        tmp_MolMod.trajectory = None #self.trajectory.extract(atoms_list)

        return tmp_MolMod

    def select_with_mdtraj(self, selection=None):
        return self.trajectory.topology_mdtraj.select(selection)

    def get_molecules(self,with_bonds=False):
        from molmodmt.formats.classes.api_mdtraj_Topology import get_molecules as _get_molecules
        return _get_molecules(self.trajectory.topology_mdtraj,with_bonds)

