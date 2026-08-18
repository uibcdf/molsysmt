from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form='file:xtc'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:xtc.

    Parameters
    ----------
    item : file:xtc
        Source item in file:xtc form.
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
        try:
            output = tmp_item.n_atoms
        except Exception:
            # We try to read coordinates of one frame to see the shape
            coords = tmp_item.read(n_frames=1)[0]
            output = coords.shape[1]
    return output

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
