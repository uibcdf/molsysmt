from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolecularMechanicsDict')
def merge(items, atom_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

