from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="mdtraj.Topology")
@dep_digest("mdtraj")
def to_mdtraj_Trajectory(
    item, atom_indices="all", coordinates=None, box=None, skip_digestion=False
):
    """
    Converting from mdtraj.Topology to mdtraj.Trajectory.


    Parameters
    ----------
    item : mdtraj.Topology
        Source topology without Cartesian coordinates.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include. Repeated indices are included once,
        in source-topology order.
    coordinates : quantity, default=None
        Cartesian coordinates with shape (n_structures, n_atoms, 3) on the full
        source atom axis. Explicit length units are required. Values are
        converted to nanometers for MDTraj. Required for trajectory construction.
    box : quantity, default=None
        Optional periodic cell vectors with shape (n_structures, 3, 3),
        one row per cell vector. Lengths are converted to nanometers.
        A single cell is shared across structures; otherwise the structure
        count must match the coordinate array.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    Raises
    ------
    ArgumentError
        If coordinates are absent, do not cover the full source atom axis, or
        the number of supplied boxes is neither one nor the structure count.

    Notes
    -----
    Atom selection follows the source-order convention of this form's topology
    extractor. Coordinate and box inputs are not modified. MDTraj stores
    coordinates in nanometers, independently of the active presentation units.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> topology = msm.convert(molsys, to_form='mdtraj.Topology')
    >>> coordinates = msm.get(molsys, coordinates=True)
    >>> trajectory = msm.convert(topology, to_form='mdtraj.Trajectory',
    ...                          coordinates=coordinates, selection=[0, 2])
    >>> trajectory.n_atoms == 2
    True

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Convert` for form-agnostic conversion and explicit
       coordinate inputs.

    .. versionadded:: 1.0.0
    """

    import numpy as np
    from mdtraj.core.trajectory import Trajectory

    from molsysmt import pyunitwizard as puw
    from molsysmt._private.smonitor import ArgumentError
    from molsysmt._private.variables import is_all

    from .extract import extract

    if coordinates is None:
        raise ArgumentError("coordinates", value=coordinates)
    positions = puw.get_value(coordinates, to_unit="nm")
    if positions.shape[1] != item.n_atoms:
        raise ArgumentError("coordinates", value=coordinates)
    topology = extract(item, atom_indices=atom_indices, skip_digestion=True)
    if not is_all(atom_indices):
        selected = set(atom_indices)
        positions = positions[
            :, [atom.index for atom in item.atoms if atom.index in selected], :
        ]
    result = Trajectory(positions, topology)
    if box is not None:
        cells = puw.get_value(box, to_unit="nm")
        if cells.shape[0] == 1 and result.n_frames != 1:
            cells = np.broadcast_to(cells, (result.n_frames, 3, 3))
        elif cells.shape[0] != result.n_frames:
            raise ArgumentError("box", value=box)
        result.unitcell_vectors = cells
    return result
