from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest(form="openmm.PDBFile")
@dep_digest("openmm")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form openmm.PDBFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to retain once each in source order, with the
        matching coordinates and internal bonds.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Model positions on the structure axis; requested order and repetitions
        are preserved. A PDBFile projection requires at least one structure.
    copy_if_all : bool, default=True
        Whether an unrestricted extraction creates an independent copy. If
        False, that unrestricted source is reused.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.PDBFile
        Resulting object in openmm.PDBFile form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        if copy_if_all:
            from copy import deepcopy

            tmp_item = deepcopy(item)
        else:
            tmp_item = item
        return tmp_item

    from copy import copy

    from molsysmt import pyunitwizard as puw

    from ..openmm_Topology.extract import extract as extract_topology
    from .get_structural_attributes import get_coordinates_from_atom

    retained = "all" if is_all(atom_indices) else sorted(set(atom_indices))
    coordinates = get_coordinates_from_atom(
        item,
        indices=retained,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    if coordinates.shape[0] == 0:
        raise NotImplementedMethodError(
            method="representing a PDBFile without a coordinate model",
            caller="molsysmt.form.openmm_PDBFile.extract",
        )
    # OpenMM has no public PDBFile projection constructor. Replace its known
    # coordinate caches together on a clone, preserving numerical precision
    # and declared bonds without a PDB write/read or full-ensemble deep copy.
    output = copy(item)
    output.topology = extract_topology(
        item.topology, atom_indices=retained, skip_digestion=True
    )
    output._positions = [
        puw.convert(row, to_unit="nm", to_form="openmm.unit") for row in coordinates
    ]
    output.positions = output._positions[0]
    output._numpyPositions = None
    return output
