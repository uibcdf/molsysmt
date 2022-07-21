from molsysm._private.exception import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='openmm.AmberPrmtopFile')
def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedMethodError()

