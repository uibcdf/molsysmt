from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native.viewer_json import ViewerJSON, _empty_structure_viewer_dict
from molsysmt import pyunitwizard as puw
import numpy as np


def _box_vectors(box):
    """Return box vectors (nm) from a 3x3 matrix."""
    arr = np.asarray(box, dtype=float)
    if arr.ndim == 2:
        arr = arr[None, ...]
    v0, v1, v2 = arr[0]
    return {
        "v0": np.asarray(v0, dtype=float).tolist(),
        "v1": np.asarray(v1, dtype=float).tolist(),
        "v2": np.asarray(v2, dtype=float).tolist(),
    }


@arg_digest(form='molsysmt.Structures')
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
                structure["box"] = _box_vectors(np.asarray(box_values[ii]))
            structures.append(structure)

    data["structures"] = structures

    return viewer
