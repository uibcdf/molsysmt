from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.coordinates.CRDReader', to_form='MDAnalysis.coordinates.CRDReader')
def add(to_item, item):

    raise NotImplementedMethodError()

