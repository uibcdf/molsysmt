from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.Topology', to_form='molsysmt.Topology')
def add(to_item, item, keep_ids=True, skip_digestion=False):

    raise NotImplementedError
