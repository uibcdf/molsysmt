"""Select sequence groups without treating characters as molecular atoms."""

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import ArgumentError, NotWithThisFormError
from molsysmt._private.variables import is_all


def extract(item, width, atom_indices, group_indices, structure_indices, *, caller):
    form = f"string:amino_acids_{width}"
    if not is_all(structure_indices):
        raise NotWithThisFormError(
            caller=caller,
            form=form,
            requested_attribute="structure_indices",
            message="Sequence forms do not contain structures.",
        )
    if not is_all(group_indices):
        if not is_all(atom_indices):
            raise ArgumentError(
                "group_indices",
                caller=caller,
                message="Use one sequence-position argument, not both.",
            )
        indices = group_indices
    else:
        indices = atom_indices
    prefix = f"amino_acids_{width}:"
    sequence = item.removeprefix(prefix)
    if len(sequence) % width:
        raise ArgumentError(
            "item",
            caller=caller,
            message="Sequence text must contain complete group codes.",
        )
    indices = flat_axis(indices, "group_indices", caller)
    if is_all(indices):
        return item
    if indices is None or any(index >= len(sequence) // width for index in indices):
        raise ArgumentError(
            "group_indices",
            caller=caller,
            message=f"Sequence positions are outside the original group axis of {form}.",
        )
    selected = "".join(
        sequence[index * width : (index + 1) * width] for index in indices
    )
    return (prefix if item.startswith(prefix) or not selected else "") + selected
