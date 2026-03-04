from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

form='mdtraj.Topology'

@arg_digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):
    raise NotImplementedMethodError()
