from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

form = "openmm.State"

###### Set

## to atom


@arg_digest(form=form)
def set_coordinates_to_atom(
    item, indices="all", value=None, structure_indices="all", skip_digestion=False
):
    """
    Refusing coordinate mutation of a captured OpenMM State.


    Parameters
    ----------
    item : openmm.State
        Captured data, which has no position mutator. Use an OpenMM Context
        or native Structures object for coordinate editing.
    indices : str or list of int, default='all'
        Requested atom positions; assignment is unavailable for this form.
    value : quantity or none, default=None
        Requested coordinates of shape (n_structures, n_atoms, 3). No values
        are assigned to the snapshot.
    structure_indices : str or list of int, default='all'
        Requested structure positions, accepted for the public set protocol.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Raises
    ------
    NotImplementedMethodError
        Always: a State snapshot cannot be edited in place.

    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError(
        method="assigning coordinates to an immutable openmm.State; use Context or Structures",
        caller="molsysmt.form.openmm_State.set_coordinates_to_atom",
    )


###
### System
###


@arg_digest(form=form)
def set_coordinates_to_system(
    item, value=None, structure_indices="all", skip_digestion=False
):
    """
    Refusing whole-system coordinate mutation of a captured State.


    Parameters
    ----------
    item : openmm.State
        Immutable captured data; edit a Context or native Structures instead.
    value : quantity or none, default=None
        Requested coordinates of shape (n_structures, n_atoms, 3). The
        snapshot is not modified.
    structure_indices : str or list of int, default='all'
        Requested structure positions, accepted for the public set protocol.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Raises
    ------
    NotImplementedMethodError
        Always: a State snapshot cannot be edited in place.

    .. versionadded:: 1.0.0
    """
    return set_coordinates_to_atom(
        item,
        indices="all",
        value=value,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
