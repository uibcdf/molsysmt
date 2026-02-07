from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.Simulation')
def append_structures(item, structure_id=None, time=None, coordinates=None, box=None, skip_digestion=False):

    raise NotImplementedMethodError()

