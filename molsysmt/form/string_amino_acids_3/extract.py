from copy import copy

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, NotWithThisFormError
from molsysmt._private.variables import is_all


@arg_digest(form="string:amino_acids_3")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
    group_indices="all",
):
    """
    Extracting a subset of elements or structures from form string:amino_acids_3.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Sequence positions selected through the generic extraction contract.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.


    .. versionadded:: 1.0.0
    """

    form = "string:amino_acids_3"

    if not is_all(structure_indices):
        raise NotWithThisFormError(
            caller="molsysmt.extract",
            form=form,
            requested_attribute="structure_indices",
            message=f"Form {form!r} does not contain structures to extract.",
        )

    if not is_all(group_indices):
        if not is_all(atom_indices):
            raise ArgumentError(
                argument="group_indices",
                value=group_indices,
                caller="molsysmt.form.string_amino_acids_3.extract",
                message="Use either 'atom_indices' or 'group_indices', not both.",
            )
        sequence_indices = group_indices
    else:
        sequence_indices = atom_indices

    if is_all(sequence_indices):
        if copy_if_all:
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:
        prefix = "amino_acids_3:" if item.startswith("amino_acids_3:") else ""
        sequence = item.removeprefix("amino_acids_3:")
        groups = [sequence[ii : ii + 3] for ii in range(0, len(sequence), 3)]
        invalid_indices = [
            int(index)
            for index in sequence_indices
            if index < 0 or index >= len(groups)
        ]
        if invalid_indices:
            raise ArgumentError(
                argument="atom_indices",
                value=sequence_indices,
                caller="molsysmt.extract",
                message=(
                    f"Form {form!r} received out-of-range sequence positions "
                    f"{invalid_indices}; valid positions are in [0, {len(groups)})."
                ),
            )
        tmp_item = prefix + "".join(groups[ii] for ii in sequence_indices)
        if not tmp_item:
            tmp_item = "amino_acids_3:"

    return tmp_item
