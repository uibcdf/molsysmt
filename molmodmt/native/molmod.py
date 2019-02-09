from .trajectory import Trajectory as _Trajectory


class MolMod():

    def __init__(self):

        self.trajectory=_Trajectory()
        self.topology=None
        self.topography=None
