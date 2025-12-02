from molsysmt._private.digestion import digest
from molsysmt.native.viewer_json import ViewerJSON, _empty_structure_viewer_dict
from molsysmt import pyunitwizard as puw
from molsysmt.pbc import get_lengths_and_angles_from_box
import numpy as np


def _box_from_matrix(box):
    """Return box lengths (nm) and angles (rad) from a 3x3 matrix."""
    box_array = np.asarray(box)
    if box_array.ndim == 2:
        box_array = box_array[None, ...]
    lengths, angles = get_lengths_and_angles_from_box(
        puw.quantity(box_array, "nanometer"), skip_digestion=True
    )
    lengths_val = puw.get_value(lengths, to_unit="nanometer")[0]
    angles_val = puw.get_value(angles, to_unit="radian")[0]
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
    """Converting a native Structures object into ViewerJSON (topology-free)."""

    viewer = ViewerJSON()
    data = viewer.data

    n_atoms = item.n_atoms
    atoms_block = data["atoms"]
    atoms_block["atom_id"] = list(range(n_atoms)) if n_atoms is not None else []
    atoms_block["atom_name"] = []
    atoms_block["group_id"] = []
    atoms_block["group_name"] = []
    atoms_block["chain_id"] = []
    atoms_block["entity_id"] = []
    atoms_block["element_symbol"] = []
    atoms_block["formal_charge"] = []

    bonds_block = data["bonds"]
    bonds_block["atom_pairs"] = []
    bonds_block["order"] = []

    coords = item.coordinates
    times = item.time
    boxes = item.box

    coords_values = puw.get_value(coords, to_unit='nanometer') if coords is not None else None
    time_values = puw.get_value(times, to_unit='picosecond') if times is not None else None
    box_values = puw.get_value(boxes, to_unit='nanometer') if boxes is not None else None

    structures = []
    if coords_values is not None:
        for ii, positions in enumerate(coords_values):
            structure = _empty_structure_viewer_dict()
            structure["coordinates"] = np.asarray(positions, dtype=float).tolist()
            if time_values is not None:
                structure["time"] = float(time_values[ii])
            if box_values is not None:
                structure["box"] = _box_from_matrix(np.asarray(box_values[ii]))
            structures.append(structure)

    data["estructures"] = structures

    return viewer
