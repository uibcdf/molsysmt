from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

form='mdtraj.Topology'

@arg_digest(form=form)
def set_atom_id_to_atom(item, indices='all', value=None, skip_digestion=False):
    """
    Setting atom id to atom on form mdtraj.Topology.

    Parameters
    ----------
    item : mdtraj.Topology
        Source item in mdtraj.Topology form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    value : object
        Argument value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()
