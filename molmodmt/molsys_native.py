class Native():

    def __init__(self,item=None,forcefield=None):

        self.topology   = None
        self.topography = None
        self.structure  = None
        self.trajectory = None
        self.forcefield = None

        if item is not None:
            from .multitool import convert as _convert
            self.topology   = _convert(item,'mdtraj.Topology')
            self.topography = _convert(item,'yank.Topography')
            self.trajectory = _convert(item,'mdtraj.Trajectory')
            self.structure  = _convert(item,'parmed.Structure')
            del(_convert)

    def get_topology(self,form='native'):
        pass

    def set_topology(self,item=None,form='native'):
        pass

    def get_positions(self,selection=None,form='native'):

        from numpy import ndarray as _np_ndarray

        if type(selection) is str:
            tmp_atoms_list = self.select(selection)
        else:
            tmp_atoms_list = selection

        return self.trajectory.atom_slice(tmp_atoms_list,inplace=False)

    def set_positions(self,positions=None):
        pass

    def apply_forcefield(self,forcefield=None):
        pass

    def convert(self,form=None):
        from .multitool import convert as _convert
        tmp_form = _convert(self,form)
        del(_convert)
        return tmp_form

    def select(self,selection=None):
        return self.topology.select(selection)

    def view(self,viewer='nglview'):
        from .multitool import view as _view
        tmp_view = _view(self,viewer)
        del(_view)
        return tmp_view

    def extract(self,selection=None):

        from .multitool import convert as _convert

        if type(selection) is str:
            tmp_atoms_list = self.select(selection)
        else:
            tmp_atoms_list = selection

        tmp_native = Native()

        tmp_native.topology = self.topology.subset(tmp_atoms_list)
        tmp_native.topography = _convert(tmp_native.topology,'yank.Topography')
        tmp_native.structure = _convert(tmp_native.topology,'parmed.Structure')
        tmp_native.trajectory = self.trajectory.atom_slice(tmp_atoms_list,inplace=False)

        del(tmp_atoms_list,_convert)

        return tmp_native

    def get_proteins(self):

        tmp_proteins=[]
        for index_chain in range(self.topology.n_chains):
            tmp_atoms_list = self.select("protein and chainid "+str(index_chain))
            if len(tmp_atoms_list):
                tmp_proteins.append(self.extract(tmp_atoms_list))

        return tmp_proteins

    def remove_solvent(self):

        pass

    def write(self,filename=None):

        from .multitool import write as _write
        return _write(self,filename)


