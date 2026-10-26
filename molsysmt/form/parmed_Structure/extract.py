import numpy as np
from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="parmed.Structure")
@dep_digest("parmed")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form parmed.Structure.


    Parameters
    ----------
    item : molecular system
        ParmEd structure to copy or subset without modifying the source.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include. Retained atoms keep source order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include. Coordinates and available cells
        follow the supplied order; a shared cell applies to every selected structure.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Selected ParmEd structure with aligned topology, coordinates and cells.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        if copy_if_all:
            from copy import deepcopy

            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:
        from copy import deepcopy

        tmp_item = deepcopy(item)
        if not is_all(atom_indices):
            from molsysmt._private.atom_indices import (
                atom_indices_to_AmberMask,
                complementary_atom_indices,
            )

            removed_atom_indices = complementary_atom_indices(item, atom_indices)
            mask = atom_indices_to_AmberMask(item, removed_atom_indices)
            tmp_item.strip(mask)
        if not is_all(structure_indices) and tmp_item.coordinates is not None:
            coordinates = tmp_item.get_coordinates("all")
            boxes = tmp_item.get_box("all")
            if boxes is not None and len(boxes) == 1:
                boxes = np.broadcast_to(boxes, (len(coordinates), 6))
            tmp_item.coordinates = coordinates[structure_indices]
            if boxes is not None:
                tmp_item.box = boxes[structure_indices]

    return tmp_item
