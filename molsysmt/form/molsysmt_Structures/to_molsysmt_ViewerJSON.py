from molsysmt._private.digestion import digest
from molsysmt.native import ViewerJSON
from molsysmt import pyunitwizard as puw
from molsysmt.pbc import get_lengths_and_angles_from_box
import numpy as np


def _box_from_matrix(box):
    """Return box lengths (nm) and angles (rad) from a 3x3 matrix."""
    lengths, angles = get_lengths_and_angles_from_box(
        puw.quantity(np.asarray(box), "nanometer"), skip_digestion=True
    )
    lengths_val = puw.get_value(lengths, to_unit="nanometer")
    angles_val = puw.get_value(angles, to_unit="radian")
    return {
        "length_v0": float(lengths_val[0]),
        "length_v1": float(lengths_val[1]),
        "length_v2": float(lengths_val[2]),
        "angle_v1_v2": float(angles_val[0]),
        "angle_v0_v2": float(angles_val[1]),
        "angle_v0_v1": float(angles_val[2]),
    }


@digest(form='molsysmt.Structures')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Convert a native Structures object into ViewerJSON (topology-free)."""

    n_atoms = item.n_atoms
    atoms_block = {
        "atom_id": list(range(n_atoms)) if n_atoms is not None else [],
        "atom_name": [],
        "group_id": [],
        "group_name": [],
        "chain_id": [],
        "entity_id": [],
        "element_symbol": [],
        "formal_charge": [],
    }

    bonds_block = {"atom_pairs": [], "order": []}

    coords = item.coordinates
    times = item.time
    boxes = item.box

    coords_values = puw.get_value(coords, to_unit='nanometer') if coords is not None else None
    time_values = puw.get_value(times, to_unit='picosecond') if times is not None else None
    box_values = puw.get_value(boxes, to_unit='nanometer') if boxes is not None else None

    frames = []
    if coords_values is not None:
        for ii, positions in enumerate(coords_values):
            frame = {"coordinates": np.asarray(positions, dtype=float).tolist()}
            if time_values is not None:
                frame["time"] = float(time_values[ii])
            if box_values is not None:
                frame["box"] = _box_from_matrix(np.asarray(box_values[ii]))
            frames.append(frame)

    data = {
        "version": "0.1",
        "atoms": atoms_block,
        "bonds": bonds_block,
        "estructures": frames,
    }

    return ViewerJSON(data=data)
