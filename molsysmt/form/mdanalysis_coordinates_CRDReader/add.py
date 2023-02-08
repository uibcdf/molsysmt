from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='mdanalysis.coordinates_CRDReader', to_form='mdanalysis.coordinates_CRDReader')
def add(to_item, item):

    raise NotImplementedMethodError()

