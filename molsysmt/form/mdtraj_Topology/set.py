from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

form='mdtraj.Topology'

@arg_digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):
    """
    Setting atom id to atom on form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    value : object, default=None
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()
