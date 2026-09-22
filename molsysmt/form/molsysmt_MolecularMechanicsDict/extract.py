from copy import deepcopy

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt._private.variables import is_all


def _take(value, indices):
    """Take positional entries without discarding the container's unit semantics."""

    if isinstance(value, list):
        return [value[index] for index in indices]
    if isinstance(value, tuple):
        return tuple(value[index] for index in indices)
    return value[indices]


@arg_digest(form="molsysmt.MolecularMechanicsDict")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form molsysmt.MolecularMechanicsDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.


    .. versionadded:: 1.0.0
    """

    form = "molsysmt.MolecularMechanicsDict"

    if not is_all(structure_indices):
        raise NotWithThisFormError(
            caller="molsysmt.extract",
            form=form,
            requested_attribute="structure_indices",
            message=f"Form {form!r} does not contain structures to extract.",
        )

    if is_all(atom_indices):
        return deepcopy(item) if copy_if_all else item

    per_atom_attributes = ("formal_charge", "partial_charge", "atom_ff_type")
    if not any(item.get(attribute) is not None for attribute in per_atom_attributes):
        raise NotWithThisFormError(
            caller="molsysmt.extract",
            form=form,
            requested_attribute="atom_indices",
            message=f"Form {form!r} has no per-atom parameters to extract.",
        )

    output = deepcopy(item)
    for attribute in per_atom_attributes:
        value = output.get(attribute)
        if value is not None:
            output[attribute] = _take(value, atom_indices)

    return output
