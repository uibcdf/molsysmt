from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="pdbfixer.PDBFixer")
@dep_digest("pdbfixer")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form pdbfixer.PDBFixer.


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
    pdbfixer.PDBFixer
        Independent copied/selected object with atom inventory and coordinates
        in the same canonical source order. Unrestricted explicit reuse returns
        the original object.


    Notes
    -----
    Selected extraction reuses this form's OpenMM Topology converter and the
    general OpenMM-to-PDBFixer reconstruction route. Coordinates carry units
    through those tools and inherit that route's PDB coordinate precision.
    Only the source object's single represented pose is available. Copying or
    extracting does not perform chemical repair, hydration or minimization.

    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        if copy_if_all:
            from copy import deepcopy

            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:
        from molsysmt.form.openmm_Topology.to_pdbfixer_PDBFixer import (
            to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer,
        )

        from . import get_coordinates_from_atom
        from .to_openmm_Topology import to_openmm_Topology

        # Topology extraction uses canonical source order; keep geometry aligned.
        if not is_all(atom_indices):
            atom_indices = sorted(atom_indices)

        coordinates = get_coordinates_from_atom(
            item,
            indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
        tmp_item = to_openmm_Topology(
            item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
        tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(
            tmp_item, coordinates=coordinates, skip_digestion=True
        )

    return tmp_item
