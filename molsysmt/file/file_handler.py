import os

_handler_form={}
_open={}
_close={}


from .handlers.mdtraj_HDF5TrajectoryFile import open_file, close_file
_handler_form['file:h5']='mdtraj.HDFTrajectoryFile'
_open['file:h5']=open_file
_close['file:h5']=close_file

class FileHandler():

    def __init__(self, absolute_path, mode):

        if mode=='auto':
            if os.path.isfile(absolute_path):
                mode = 'read'
            else:
                mode = 'write'

        from molsysmt import get_form, convert

        self.absolute_path = absolute_path
        self.form = get_form(absolute_path)
        self.mode = mode
        self.read = False
        self.write = False
        
        if self.mode=='read': self.read = True
        if self.mode=='write': self.write = True

        self.handler = _open[self.form](self.absolute_path, mode=self.mode)
        self.handler_form = _handler_form[self.form]

    def close(self):

        return _close[self.form](self.handler)
