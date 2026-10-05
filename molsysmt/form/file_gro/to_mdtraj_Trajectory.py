from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:gro")
@dep_digest("mdtraj")
def to_mdtraj_Trajectory(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from file:gro to mdtraj.Trajectory.

    Coordinates, times and boxes are read by MDTraj. Connectivity is obtained
    through the native GRO conversion, using MolSysMT's existing template and
    distance-based candidate rules on the first structure before selection.
    GRO does not declare bonds; the resulting graph is inferred, not a
    certification of complete chemistry. All coordinate structures are retained
    unless explicitly selected.


    Parameters
    ----------
    item : molecular system
        Path to a GRO file declaring atom/group labels, coordinates and box data.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source atom indices to retain after full-system connectivity inference.
        Defaults to 'all'.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source structure indices to retain. Defaults to 'all'. Connectivity is
        inferred using the first structure before this selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> trajectory = msm.convert(msm.systems['nglview']['md_1u19.gro'],
    ...                         to_form='mdtraj.Trajectory', selection=[0, 1])
    >>> trajectory.xyz.shape
    (1, 2, 3)

    .. admonition:: User guide

       See :ref:`user-foundations-native-world-file-handlers-molsysmt-grofilehandler`
       for connectivity and coordinate-reading limits.

    .. versionadded:: 1.0.0
    """

    from mdtraj import load

    from ..mdtraj_Trajectory.extract import extract
    from ..molsysmt_Topology.to_mdtraj_Topology import (
        to_mdtraj_Topology as native_to_mdtraj,
    )
    from .to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = load(item)
    native_topology = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item.topology = native_to_mdtraj(native_topology, skip_digestion=True)
    tmp_item = extract(
        tmp_item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    return tmp_item
