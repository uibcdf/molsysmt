from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest
import types

form='file:dcd'

@arg_digest(form=form)
@dep_digest('mdtraj')
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:dcd.

    Parameters
    ----------
    item : file:dcd
        Source item in file:dcd form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    from mdtraj.formats import DCDTrajectoryFile
    from molsysmt._private.backend_output import silence_backend_stdout
    from molsysmt._private.files_and_directories import str_filename

    with silence_backend_stdout(), DCDTrajectoryFile(str_filename(item), mode='r') as handle:
        coordinates = handle.read(n_frames=1)[0]
    return coordinates.shape[1]

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
