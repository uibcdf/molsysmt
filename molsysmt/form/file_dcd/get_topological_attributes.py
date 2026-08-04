from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest
import types

form='file:dcd'

@arg_digest(form=form)
@dep_digest('mdtraj')
def get_n_atoms_from_system(item, skip_digestion=False):
    """Reading the atom count through MDTraj's endian-aware DCD reader."""

    from mdtraj.formats import DCDTrajectoryFile
    from molsysmt._private.backend_output import silence_backend_stdout
    from molsysmt._private.files_and_directories import str_filename

    with silence_backend_stdout(), DCDTrajectoryFile(str_filename(item), mode='r') as handle:
        coordinates = handle.read(n_frames=1)[0]
    return coordinates.shape[1]

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
