from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='bcifreader.PdbxContainers.DataContainer', to_form='bcifreader.PdbxContainers.DataContainer')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

