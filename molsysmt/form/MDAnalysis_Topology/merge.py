from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.Topology')
def merge(items, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

