from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt._private.variables import is_all
import types

form = 'mdtraj.PDBTrajectoryFile'

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom index from atom in form mdtraj.PDBTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        return list(range(item.topology.n_atoms))
    return list(indices)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    """
    Getting n atoms from system in form mdtraj.PDBTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return item.topology.n_atoms

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form mdtraj.PDBTrajectoryFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotWithThisFormError(caller='molsysmt.form.mdtraj_PDBTrajectoryFile.get_n_groups_from_system', form=form, requested_attribute='n_groups', message='This form does not expose group-level topology directly. Please convert to a topology-enabled form first.')

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
