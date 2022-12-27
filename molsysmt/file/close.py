import os

def _close_mdtraj_HDF5TrajectoryFile(item):
    item.close()
    pass


_close={}
_close['mdtraj.HDF5TrajectoryFile']=_close_mdtraj_HDF5TrajectoryFile

def close(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import handler

    file_handler = handler.pop(absolute_path)

    _close[file_handler.handler_form](file_handler.handler)

    del file_handler

    pass

