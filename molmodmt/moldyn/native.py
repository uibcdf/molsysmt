class Native():

    def __init__(self,item=None,molsystem=None):

        self.trajectory = None
        self.molsystem  = None

        from molsysmt.multitool import load as _molsystem_load
        from .multitool import convert as _convert

        if molsystem is not None:
            self.molsystem = _molsystem_load(molsystem)
        elif item is not None:
            self.molsystem = _molsystem_load(item)

        if item is not None:
            self.trajectory = _convert(item,'mdtraj.Trajectory')

        del(_convert,_molsystem_load)

    def convert(self,form=None):

        from .multitool import convert as _convert
        tmp_form = _convert(self,form)
        del(_convert)
        return tmp_form

        pass

    def select(self, selection=None):

        return self.molsystem.select(selection)

    def view(self,viewer='nglview'):
        from .multitool import view as _view
        tmp_view = _view(self,viewer)
        del(_view)
        return tmp_view

    def get_trajectory(self,form='native.Native'):

        pass

    def get_positions(self,form='native.Native'):

        pass

    def set_trajectory(self):

        pass

    def set_positions(self):

        pass

    def get_topology(self):

        pass

    def set_topology(self):

        pass

