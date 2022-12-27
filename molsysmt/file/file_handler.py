import os

handler_form={
        'file:h5': 'mdtraj.HDF5TrajectoryFile',
        }

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
        self.handler_form = handler_form[self.form]
        self.mode = mode
        self.read = False
        self.write = False
        
        if self.mode=='read': self.read = True
        if self.mode=='write': self.write = True

        self.handler = convert(self.absolute_path, to_form=self.handler_form, mode=self.mode)

