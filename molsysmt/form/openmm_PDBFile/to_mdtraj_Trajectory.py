from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest

from .get_structural_attributes import get_box_from_system, get_coordinates_from_atom


@arg_digest(form="openmm.PDBFile")
@dep_digest("mdtraj")
def to_mdtraj_Trajectory(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from openmm.PDBFile to mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom positions to retain once each in source order.
    structure_indices : str or list of int, default='all'
        PDB models to retain, preserving request order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    from molsysmt import pyunitwizard as puw
    from molsysmt._private.variables import is_all
    from molsysmt.form.openmm_Topology.to_mdtraj_Topology import to_mdtraj_Topology

    if not is_all(atom_indices):
        atom_indices = sorted(set(atom_indices))
    topology = to_mdtraj_Topology(
        item.topology, atom_indices=atom_indices, skip_digestion=True
    )
    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    positions = puw.get_value(coordinates, to_unit="nanometers")
    tmp_item = mdtraj_Trajectory(positions, topology)
    box = get_box_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    if box is not None:
        tmp_item.unitcell_vectors = puw.get_value(box, to_unit="nm")

    return tmp_item
