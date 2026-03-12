from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import types

form = 'file:h5'

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    import mdtraj as md
    with md.open(item) as tmp_item:
        # mdtraj HDF5TrajectoryFile uses __len__ for n_frames
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
