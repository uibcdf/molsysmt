from molsysmt._private.digestion import digest
from molsysmt.native import ViewerJSON
from molsysmt import pyunitwizard as puw
import numpy as np


def _angles_from_box(box):
    a_vec, b_vec, c_vec = box
    a = np.linalg.norm(a_vec)
    b = np.linalg.norm(b_vec)
    c = np.linalg.norm(c_vec)
    alpha = np.degrees(np.arccos(np.dot(b_vec, c_vec) / (b * c)))
    beta = np.degrees(np.arccos(np.dot(a_vec, c_vec) / (a * c)))
    gamma = np.degrees(np.arccos(np.dot(a_vec, b_vec) / (a * b)))
    return dict(a=float(a), b=float(b), c=float(c), alpha=float(alpha), beta=float(beta), gamma=float(gamma))


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

    bonds_block = {"indexA": [], "indexB": [], "order": []}

    coords = item.coordinates
    times = item.time
    boxes = item.box

    coords_values = puw.get_value(coords, to_unit='nanometer') if coords is not None else None
    time_values = puw.get_value(times, to_unit='picosecond') if times is not None else None
    box_values = puw.get_value(boxes, to_unit='nanometer') if boxes is not None else None

    frames = []
    if coords_values is not None:
        for ii, positions in enumerate(coords_values):
            frame = {"positions": np.asarray(positions, dtype=float).tolist()}
            if time_values is not None:
                frame["time"] = float(time_values[ii])
            if box_values is not None:
                frame["cell"] = _angles_from_box(np.asarray(box_values[ii]))
            frames.append(frame)

    data = {
        "version": "0.1",
        "atoms": atoms_block,
        "bonds": bonds_block,
        "estructures": frames,
    }

    return ViewerJSON(data=data)
