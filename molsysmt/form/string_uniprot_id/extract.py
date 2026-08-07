from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:uniprot_id')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    raise NotImplementedMethodError()
