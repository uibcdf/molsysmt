from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
import types

form = 'mdtraj.DCDTrajectoryFile'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form mdtraj.DCDTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.DCDTrajectoryFile
        Source item in mdtraj.DCDTrajectoryFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    position = item.tell()
    try:
        item.seek(0)
        coordinates = item.read(n_frames=1)[0]
    finally:
        item.seek(position)
    return coordinates.shape[1]

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form mdtraj.DCDTrajectoryFile.

    Parameters
    ----------
    item : mdtraj.DCDTrajectoryFile
        Source item in mdtraj.DCDTrajectoryFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    raise NotWithThisFormError(caller='molsysmt.form.mdtraj_DCDTrajectoryFile.get_n_groups_from_system', form=form, requested_attribute='n_groups', message='This form does not store topology information directly. Please convert to a topology-enabled form first.')

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
