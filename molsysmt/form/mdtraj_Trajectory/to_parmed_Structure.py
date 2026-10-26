import numpy as np
from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="mdtraj.Trajectory")
@dep_digest("parmed")
@dep_digest("openmm")
def to_parmed_Structure(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from mdtraj.Trajectory to parmed.Structure.


    Parameters
    ----------
    item : molecular system
        MDTraj trajectory supplying topology, coordinates and optional unit cells.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include. Selected atoms retain source order;
        repeated indices are included once.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include, preserving the supplied order.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Topology with all selected coordinates and available cells. ParmEd stores
        lengths in angstroms and cell angles in degrees. Force-field parameters
        are not inferred from MDTraj topology.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.convert(msm.systems['Trp-Cage']['1l2y.pdb'],
    ...                      to_form='mdtraj.Trajectory', structure_indices=[0])
    >>> converted = to_parmed_Structure(source)
    >>> np.allclose(converted.get_coordinates('all'), source.xyz * 10)
    True

    .. versionadded:: 1.0.0
    """

    from molsysmt import pyunitwizard as puw
    from molsysmt._private.variables import is_all
    from molsysmt.form.mdtraj_Topology.to_parmed_Structure import (
        to_parmed_Structure as topology_to_parmed_Structure,
    )
    from molsysmt.pbc import get_lengths_and_angles_from_box

    from . import get_box_from_system, get_coordinates_from_atom

    if not is_all(atom_indices):
        atom_indices = np.unique(np.asarray(atom_indices, dtype=np.int64))

    tmp_item = topology_to_parmed_Structure(
        item.topology, atom_indices=atom_indices, skip_digestion=True
    )
    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.coordinates = puw.get_value(coordinates, to_unit="angstrom")
    box = get_box_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    if box is not None:
        lengths, angles = get_lengths_and_angles_from_box(box, skip_digestion=True)
        tmp_item.box = np.column_stack(
            (
                puw.get_value(lengths, to_unit="angstrom"),
                puw.get_value(angles, to_unit="degrees"),
            )
        )

    return tmp_item
