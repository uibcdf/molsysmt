import numpy as np  # noqa: F401

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all

form = "openmm.Context"

###### Set

## to atom


@arg_digest(form=form)
def set_coordinates_to_atom(
    item, indices="all", value=None, structure_indices="all", skip_digestion=False
):
    """
    Setting coordinates to atom on form openmm.Context.


    Parameters
    ----------
    item : openmm.Context
        Live simulation context whose current positions will be changed.
    indices : str or list of int, default='all'
        Atom positions to update. Other atoms retain their current positions.
    value : quantity or none, default=None
        Length coordinates of shape (1, n_selected_atoms, 3), converted to
        OpenMM nm before assignment.
    structure_indices : str or list of int, default='all'
        The current structure, either 'all' or [0]. A Context stores one pose.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    if (not is_all(structure_indices) and list(structure_indices) != [0]) or (
        value is not None and len(value) != 1
    ):
        raise NotImplementedMethodError(
            method="assigning multiple or absent structures to an openmm.Context",
            caller="molsysmt.form.openmm_Context.set_coordinates_to_atom",
        )
    value = puw.convert(value[0], to_unit="nanometers", to_form="openmm.unit")

    if is_all(indices):
        item.setPositions(value)
    else:
        positions = item.getState(getPositions=True).getPositions(asNumpy=True)
        positions[indices, :] = value
        item.setPositions(positions)

    pass


###
### System
###


@arg_digest(form=form)
def set_coordinates_to_system(
    item, value=None, structure_indices="all", skip_digestion=False
):
    """
    Setting coordinates to system on form openmm.Context.


    Parameters
    ----------
    item : openmm.Context
        Live simulation context whose current positions will be changed.
    value : quantity or none, default=None
        Length coordinates of shape (1, n_atoms, 3), converted to OpenMM nm.
    structure_indices : str or list of int, default='all'
        The current structure, either 'all' or [0]. A Context stores one pose.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """
    return set_coordinates_to_atom(
        item,
        indices="all",
        value=value,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
