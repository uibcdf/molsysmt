from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form='file:h5'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    import mdtraj as md
    tmp_item = md.open(item)
    # mdtraj HDF5TrajectoryFile has no n_atoms, we check the first frame
    try:
        output = tmp_item.n_atoms
    except:
        # We try to read coordinates of one frame to see the shape
        coords = tmp_item.read(n_frames=1)[0]
        output = coords.shape[1]
    tmp_item.close()
    return output

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
