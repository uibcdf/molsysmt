from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest(form="openmm.Modeller")
@dep_digest("openmm")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to retain once each in source order. Coordinates
        follow that same atom axis.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        The single structure, either 'all' or [0]. Multiple structures cannot
        be represented by a Modeller and are rejected.
    copy_if_all : bool, default=True
        Whether an unrestricted extraction returns an independent topology and
        positions. If False, the unrestricted source is reused.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import Modeller

    from molsysmt import pyunitwizard as puw

    from ..openmm_Topology.extract import extract as extract_openmm_Topology
    from .get_structural_attributes import get_coordinates_from_atom

    if not is_all(structure_indices):
        if len(structure_indices) != 1 or structure_indices[0] != 0:
            raise NotImplementedMethodError(
                method="representing multiple or absent structures in openmm.Modeller",
                caller="molsysmt.form.openmm_Modeller.extract",
            )
    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    retained = "all" if is_all(atom_indices) else sorted(set(atom_indices))
    topology = extract_openmm_Topology(
        item.topology, atom_indices=retained, skip_digestion=True
    )
    coordinates = get_coordinates_from_atom(
        item, indices=retained, structure_indices=[0], skip_digestion=True
    )
    positions = puw.convert(coordinates[0], to_unit="nm", to_form="openmm.unit")
    return Modeller(topology, positions)
