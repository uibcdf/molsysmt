from molsysmt._private.argdigest import arg_digest

from .get_structural_attributes import (
    get_coordinates_from_atom,
)


@arg_digest(form="openmm.PDBFile")
def to_openmm_Modeller(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from openmm.PDBFile to openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom positions to retain once each in source order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        The first selected model supplies the single Modeller pose. The
        default 'all' uses model 0. No trajectory is retained by this target.
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
    from molsysmt._private.smonitor import NotImplementedMethodError
    from molsysmt._private.variables import is_all
    from molsysmt.form.openmm_Topology.extract import extract as extract_topology

    if not is_all(atom_indices):
        atom_indices = sorted(set(atom_indices))
    selected = [0] if is_all(structure_indices) else structure_indices[:1]
    if len(selected) == 0:
        raise NotImplementedMethodError(
            method="constructing an openmm.Modeller without a structure",
            caller="molsysmt.form.openmm_PDBFile.to_openmm_Modeller",
        )
    topology = extract_topology(
        item.topology, atom_indices=atom_indices, skip_digestion=True
    )

    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=selected,
        skip_digestion=True,
    )
    positions = puw.convert(coordinates[0], "nm", to_form="openmm.unit")
    tmp_item = Modeller(topology, positions)

    return tmp_item
