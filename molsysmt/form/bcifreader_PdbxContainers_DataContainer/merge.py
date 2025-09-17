from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mmcif.PdbxContainers.DataContainer')
def merge(items, atom_indices='all', structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

