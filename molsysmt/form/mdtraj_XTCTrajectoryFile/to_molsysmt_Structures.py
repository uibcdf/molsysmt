import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="mdtraj.XTCTrajectoryFile")
def to_molsysmt_Structures(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from mdtraj.XTCTrajectoryFile to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import Structures

    from .get_topological_attributes import get_n_atoms_from_system
    from .iterators import StructuresIterator

    if is_all(structure_indices):
        # A complete output can use the provider's vectorized bulk reader.
        position = item.tell()
        try:
            item.seek(0)
            coordinates, time, labels, box = item.read(
                atom_indices=None if is_all(atom_indices) else atom_indices
            )
        finally:
            item.seek(position)
        return Structures(
            coordinates=puw.quantity(coordinates, "nm"),
            time=None if time is None else puw.quantity(time, "ps"),
            structure_id=labels,
            box=None if box is None or len(box) == 0 else puw.quantity(box, "nm"),
        )

    # Read selected structures through the existing seek-based iterator rather
    # than materializing the complete source and slicing afterwards.
    iterator = StructuresIterator(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        coordinates=True,
        box=True,
        time=True,
        structure_id=True,
        output_type="dictionary",
        skip_digestion=True,
    )
    rows = {name: [] for name in ("coordinates", "box", "time", "structure_id")}
    available = {name: True for name in rows}
    units = {"coordinates": "nm", "box": "nm", "time": "ps"}
    position = item.tell()
    try:
        for block in iterator:
            for name in rows:
                value = block[name]
                if value is None:
                    available[name] = False
                elif available[name]:
                    values = (
                        puw.get_value(value, to_unit=units[name])
                        if name in units
                        else value
                    )
                    rows[name].append(np.asarray(values)[0])
    finally:
        item.seek(position)

    if not rows["coordinates"]:
        n_atoms = (
            get_n_atoms_from_system(item, skip_digestion=True)
            if is_all(atom_indices)
            else len(atom_indices)
        )
        return Structures(coordinates=puw.quantity(np.empty((0, n_atoms, 3)), "nm"))

    payload = {}
    for name, values in rows.items():
        if not available[name]:
            payload[name] = None
        elif name in units:
            payload[name] = puw.quantity(np.asarray(values), units[name])
        else:
            payload[name] = np.asarray(values)
    return Structures(**payload)
