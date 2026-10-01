import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest()
@attributed("hbonds", "luzar_chandler")
def get_luzard_chandler_hbonds(
    molecular_system,
    selection="all",
    acceptors=None,
    donors=None,
    structure_indices="all",
    molecular_system_2=None,
    selection_2=None,
    acceptors_2=None,
    donors_2=None,
    structure_indices_2=None,
    distance_threshold="3.5 angstroms",
    angle_threshold="30 degrees",
    pbc=True,
    syntax="MolSysMT",
    output_type="tuple",
    skip_digestion=False,
):
    """
    Calculating hydrogen bonds using the Luzard–Chandler geometric criteria.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    acceptors : numpy.ndarray, list, or tuple, default=None
        Precomputed atom indices of hydrogen bond acceptors.
    donors : numpy.ndarray, list, or tuple, default=None
        Precomputed atom indices of hydrogen bond donors.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    molecular_system_2 : object, default=None
        A second molecular system is not supported by this method.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    acceptors_2 : numpy.ndarray, list, or tuple, default=None
        Precomputed acceptor atom indices for selection_2.
    donors_2 : numpy.ndarray, list, or tuple, default=None
        Precomputed donor atom indices for selection_2.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    distance_threshold : quantity, default='3.5 angstroms'
        Maximum donor-to-acceptor separation; equivalent to 0.35 nm.
    angle_threshold : quantity, default='30 degrees'
        Strict upper bound for the H-D-A angle, with the donor as vertex.
        Equivalent to pi/6 radians.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    output_type : {'tuple', 'molsysmt.Interactions'}, default='tuple'
        Return the established triples, distances, and angles, or a sparse
        analysis with evaluated coverage, participant scope, producer versions,
        and periodic images. The analysis requires automatically identified
        roles and one selection, two disjoint participant universes, or
        identical role selections.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    tuple or molsysmt.Interactions
        By default, ``(atoms, distances, angles)`` in requested structure order.
        Equal counts give an int64 array of shape ``(n_structures, n_hbonds, 3)``
        and quantities of shape ``(n_structures, n_hbonds)`` in nm and radians.
        Varying counts give aligned lists of ``(n_hbonds, 3)`` triple arrays
        and ``(n_hbonds,)`` quantities, including shaped empty entries.
        Triples use donor, hydrogen, acceptor order and original atom indices.
        The optional analysis preserves original local axes and deduplicates
        repeated requested structures. Its distance is D-A and its angle is H-D-A.

    Raises
    ------
    NotImplementedMethodError
        If a second molecular system is supplied, or the optional analysis
        uses supplied role arrays, a second structure axis, or partially
        overlapping participant universes.
    InternalAlgorithmError
        If observed periodic images disagree with the detector's D-A
        distances or H-D-A angles.

    Notes
    -----
    The result is independent and is not automatically attached to the system.
    With PBC, donor-anchored D-H and D-A images reproduce the two minimum-image
    vectors used for the angle. The optional analysis records the
    calculation-time MolSysMT version in ``software``. This method uses eager
    execution and does not stream large trajectories.
    The optional analysis records the luzar_chandler criterion and original
    paper in its parameters. Completed calculations contribute to an optional
    Ackredit workflow session; tuple outputs keep their existing layout.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.interactions.hbonds.get_luzard_chandler_hbonds import get_luzard_chandler_hbonds
    >>> molsys = msm.convert(msm.systems["chicken villin HP35"][
    ...     "chicken_villin_HP35.h5msm"], to_form="molsysmt.MolSys")
    >>> result = get_luzard_chandler_hbonds(molsys, selection=[0],
    ...     output_type="molsysmt.Interactions")
    >>> result.n_interactions
    0
    >>> result.measure_units
    {'distance': 'nm', 'angle': 'rad'}

    .. admonition:: User guide

       See :ref:`Tutorial_Get_luzard_chandler_hbonds` for both geometric criteria
       and :ref:`user-tools-interactions-result` for sparse queries and persistence.

    .. versionadded:: 1.0.0
    """

    from molsysmt import pyunitwizard as puw
    from molsysmt.basic import get, select
    from molsysmt.structure import get_angles, get_neighbors

    from ._empty_result import pack_result
    from ._to_interactions import to_luzard_chandler_interactions
    from .get_acceptor_atoms import get_acceptor_atoms
    from .get_donor_atoms import get_donor_atoms

    if molecular_system_2 is not None:
        raise NotImplementedMethodError(
            caller="molsysmt.interactions.hbonds.get_luzard_chandler_hbonds")
    return_interactions = output_type == "molsysmt.interactions"
    if return_interactions and any(value is not None for value in (
        acceptors, donors, acceptors_2, donors_2, structure_indices_2,
    )):
        raise NotImplementedMethodError(
            method="Luzard-Chandler Interactions output",
            arguments="supplied roles or a second structure axis",
            caller="molsysmt.interactions.hbonds.get_luzard_chandler_hbonds",
        )

    angle_threshold = puw.standardize(angle_threshold)
    if is_all(structure_indices):
        structure_indices = np.arange(get(molecular_system, n_structures=True))
    else:
        structure_indices = np.atleast_1d(structure_indices)

    def roles(selected, donor_pairs, acceptor_indices):
        if acceptor_indices is None:
            acceptor_indices = get_acceptor_atoms(
                molecular_system, selection=selected, syntax=syntax)
        else:
            acceptor_indices = select(
                molecular_system, selection=selected, mask=acceptor_indices, syntax=syntax)
        if donor_pairs is None:
            donor_pairs = get_donor_atoms(molecular_system, selection=selected, syntax=syntax)
        else:
            donor_pairs = select(
                molecular_system, selection=selected, mask=donor_pairs, syntax=syntax)
        return donor_pairs, acceptor_indices

    donors, acceptors = roles(selection, donors, acceptors)
    two_selections = any(value is not None for value in (selection_2, acceptors_2, donors_2))
    directions = [(donors, acceptors)]
    if two_selections:
        if selection_2 is None:
            selection_2 = selection
        donors_2, acceptors_2 = roles(selection_2, donors_2, acceptors_2)
        directions = [(donors, acceptors_2), (donors_2, acceptors)]

    searches = []
    for donor_pairs, acceptor_indices in directions:
        unique_donors, donor_restore = np.unique(donor_pairs[:, 0], return_inverse=True)
        if not len(unique_donors) or not len(acceptor_indices) or not len(structure_indices):
            neighbors = (
                np.zeros(len(structure_indices) * len(unique_donors) + 1, dtype=np.int64),
                np.empty(0, dtype=np.int64), puw.quantity(np.empty(0), "nanometers"),
            )
        else:
            neighbors = get_neighbors(
                molecular_system, selection=unique_donors, selection_2=acceptor_indices,
                structure_indices=structure_indices, structure_indices_2=structure_indices_2,
                threshold=distance_threshold, pbc=pbc, output_type="csr",
            )
        searches.append((donor_pairs, acceptor_indices, donor_restore,
                         len(unique_donors), *neighbors))

    output_atoms, output_distances, output_angles = [], [], []
    for position, frame in enumerate(structure_indices):
        triples, distances = [], []
        for donor_pairs, acceptor_indices, restore, n_unique, offsets, indices, values in searches:
            for pair_index, (donor, hydrogen) in enumerate(donor_pairs):
                row = position * n_unique + restore[pair_index]
                for neighbor in range(offsets[row], offsets[row + 1]):
                    acceptor = acceptor_indices[indices[neighbor]]
                    if donor != acceptor:
                        triples.append([donor, hydrogen, acceptor])
                        distances.append(values[neighbor])
        triples = np.asarray(triples, dtype=np.int64).reshape(-1, 3)
        distances = (puw.utils.sequences.concatenate(distances, value_type="numpy.ndarray")
                     if distances else puw.quantity(np.empty(0), "nanometers"))
        angles = (get_angles(molecular_system, triples[:, [1, 0, 2]],
                             pbc=pbc, structure_indices=int(frame))[0]
                  if len(triples) else puw.quantity(np.empty(0), "radians"))
        accepted = angles < angle_threshold
        output_atoms.append(triples[accepted])
        output_distances.append(distances[accepted])
        output_angles.append(angles[accepted])

    result = pack_result(output_atoms, output_distances, output_angles)
    if return_interactions:
        return to_luzard_chandler_interactions(
            molecular_system, structure_indices, donors, acceptors, *result,
            distance_threshold, angle_threshold, pbc,
            donors_2 if two_selections else None, acceptors_2 if two_selections else None,
        )
    return result
