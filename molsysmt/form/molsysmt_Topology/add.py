from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology', to_form='molsysmt.Topology')
def add(to_item, item, keep_ids=True, skip_digestion=False):

    raise NotImplementedError
