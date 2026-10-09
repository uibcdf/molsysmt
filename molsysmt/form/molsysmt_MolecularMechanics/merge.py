import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralAttributeDropWarning,
    warn,
)
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.MolecularMechanics")
def merge(items, atom_indices="all", skip_digestion=False):
    """
    Merging multiple items into a single item of form molsysmt.MolecularMechanics.

    Parameters
    ----------
    items : list of object
        List of items to merge.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanics
        Resulting object in molsysmt.MolecularMechanics form.

    Notes
    -----
    Native partial-charge columns contain numerical values in elementary charge,
    independently of the session's output units. Each column is concatenated in
    input and selection order when every contributing input provides it. A column
    absent from a contributing input is cleared, with a warning if values are lost.
    Empty selections do not contribute. Scalar settings are copied from the first
    input. Named charge/type assignment reports are cleared with a warning when
    combining inputs or selecting atoms: they do not describe a joint calculation.
    A single full input retains detached copies of its reports.

    .. versionadded:: 1.0.0
    """

    output = items[0].copy()

    n_items = len(items)

    if is_all(atom_indices):
        atom_indices = ["all" for ii in range(n_items)]

    if len(atom_indices) != n_items:
        raise ArgumentError(
            "atom_indices",
            value=atom_indices,
            caller="molsysmt.form.molsysmt_MolecularMechanics.merge",
        )

    if n_items == 1 and is_all(atom_indices[0]):
        return output

    list_formal_charge = []
    list_partial_charge = []
    list_atom_ff_type = []

    for aux_item, aux_atom_indices in zip(items, atom_indices):
        if is_all(aux_atom_indices):
            list_formal_charge.append(aux_item.formal_charge)
            list_partial_charge.append(aux_item.partial_charge)
            list_atom_ff_type.append(aux_item.atom_ff_type)

        else:
            if len(aux_atom_indices) > 0:
                fc = aux_item.formal_charge
                list_formal_charge.append(
                    fc[aux_atom_indices] if fc is not None else None
                )

                pc = aux_item.partial_charge
                list_partial_charge.append(
                    pc[aux_atom_indices] if pc is not None else None
                )

                aft = aux_item.atom_ff_type
                list_atom_ff_type.append(
                    aft[aux_atom_indices] if aft is not None else None
                )

    # The first input's row count cannot constrain the combined atom axis.
    output.atoms_ff = None
    dropped = []
    for name, columns in (
        ("formal_charge", list_formal_charge),
        ("partial_charge", list_partial_charge),
        ("atom_ff_type", list_atom_ff_type),
    ):
        if columns and all(column is not None for column in columns):
            setattr(output, name, np.concatenate(columns))
        elif any(column is not None for column in columns):
            dropped.append(name)

    for name in ("partial_charge_assignment", "atom_type_assignment"):
        if any(getattr(item, name, None) is not None for item in items):
            dropped.append(name)
        setattr(output, name, None)
    if dropped:
        warn(
            StructuralAttributeDropWarning(attributes=dropped, caller="molsysmt.merge"),
            stacklevel=2,
        )

    return output
