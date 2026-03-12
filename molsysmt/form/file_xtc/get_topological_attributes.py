from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form='file:xtc'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
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
