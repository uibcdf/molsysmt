from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import types

form = 'file:xtc'

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    """
    Getting n structures from system in form file:xtc.

    Parameters
    ----------
    item : file:xtc
        Source item in file:xtc form.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    import mdtraj as md
    with md.open(item) as tmp_item:
        # mdtraj XTCTrajectoryFile uses __len__ for n_frames
        try:
            output = len(tmp_item)
        except Exception:
            coords = tmp_item.read(n_frames=1)[0]
            output = coords.shape[1]
    if not is_all(structure_indices):
        output = len(structure_indices)
    return output

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
