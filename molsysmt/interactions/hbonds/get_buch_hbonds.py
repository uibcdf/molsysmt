import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest()
@attributed("hbonds", "hydrogen_acceptor_distance")
def get_buch_hbonds(
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
    distance_threshold="2.3 angstroms",
    pbc=True,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    output_type="tuple",
):
    """
    Calculating hydrogen bonds using the Buch geometric criteria.


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
    distance_threshold : quantity, default='2.3 angstroms'
        Maximum hydrogen-to-acceptor separation; equivalent to 0.23 nm.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    output_type : {'tuple', 'molsysmt.Interactions'}, default='tuple'
        Return the established triples and distances, or a sparse analysis
        with evaluated coverage, participant scope, and periodic images.
        The analysis currently requires automatically identified roles and
        one selection, two disjoint participant universes, or identical
        role selections.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    tuple or molsysmt.Interactions
        By default, ``(atoms, distances)`` in requested structure order.
        Equal per-structure counts give an integer array with shape
        ``(n_structures, n_hbonds, 3)`` and a nanometer distance quantity with
        shape ``(n_structures, n_hbonds)``. Varying counts give aligned lists
        of ``(n_hbonds, 3)`` arrays and ``(n_hbonds,)`` quantities, including
        shaped empty entries. Triples use donor, hydrogen, acceptor order
        and original system atom indices. The optional sparse analysis
        preserves original atom and structure indices and deduplicates
        repeated requested structures.

    Raises
    ------
    NotImplementedMethodError
        If a second molecular system is supplied, or the optional analysis
        uses supplied role arrays, a second structure axis, or partially
        overlapping participant universes.
    InternalAlgorithmError
        If observed periodic images disagree with the detected H-A distances
        or cannot be represented with int32 lattice shifts.

    Notes
    -----
    Detection uses explicitly represented donor-hydrogen pairs. A hydrogen-free
    input yields the documented empty result and evaluated coverage without
    reconstructing missing hydrogens. This result records the supplied model's
    available evidence; interpretation requires its hydrogen inventory.
    The detector returns an independent analysis. Attach it to
    ``molsys.interactions`` under an explicit name to retain it with the system.
    This method uses eager execution and does not stream large trajectories.
    The optional analysis records the calculation-time MolSysMT version in
    ``software``; serialization preserves it independently of the reader version.
    Its parameters retain the descriptive hydrogen_acceptor_distance criterion
    and a bibliography without inventing an unverified original Buch paper.
    Completed calculations contribute to an optional Ackredit workflow session;
    tuple outputs retain their existing layout without embedded metadata.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.interactions.hbonds.get_buch_hbonds import get_buch_hbonds
    >>> molsys = msm.convert(msm.systems["chicken villin HP35"][
    ...     "chicken_villin_HP35.h5msm"], to_form="molsysmt.MolSys")
    >>> result = get_buch_hbonds(molsys, selection=[0],
    ...                         output_type="molsysmt.Interactions")
    >>> result.n_interactions
    0

    .. admonition:: User guide

       See :ref:`Tutorial_Get_buch_hbonds` for the distance criterion and
       :ref:`user-tools-interactions-result` for sparse queries and persistence.

    .. versionadded:: 1.0.0
    """

    from molsysmt import pyunitwizard as puw
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get, select
    from molsysmt.structure import get_neighbors

    from ._empty_result import empty_result, pack_result
    from ._to_interactions import to_buch_interactions
    from .get_acceptor_atoms import get_acceptor_atoms
    from .get_donor_atoms import get_donor_atoms

    return_interactions = output_type == "molsysmt.interactions"
    if return_interactions and any(
        value is not None
        for value in (
            acceptors,
            donors,
            acceptors_2,
            donors_2,
            structure_indices_2,
        )
    ):
        raise NotImplementedMethodError(
            method="Buch Interactions output",
            arguments="supplied roles or a second structure axis",
            caller="molsysmt.interactions.hbonds.get_buch_hbonds",
        )

    def deliver(
        result,
        donor_pairs,
        acceptor_indices,
        donor_pairs_2=None,
        acceptor_indices_2=None,
    ):
        if return_interactions:
            return to_buch_interactions(
                molecular_system,
                structure_indices,
                donor_pairs,
                acceptor_indices,
                *result,
                distance_threshold,
                pbc,
                donor_pairs_2,
                acceptor_indices_2,
            )
        return result

    def neighbors(hydrogens, acceptor_atoms):
        if len(hydrogens) == 0 or len(acceptor_atoms) == 0:
            n_frames = (
                get(molecular_system, n_structures=True)
                if is_all(structure_indices)
                else len(np.atleast_1d(structure_indices))
            )
            return (
                np.zeros(n_frames * len(hydrogens) + 1, dtype=np.int64),
                np.empty(0, dtype=np.int64),
                puw.quantity(np.empty(0), "nanometers"),
            )
        return get_neighbors(
            molecular_system,
            selection=hydrogens,
            selection_2=acceptor_atoms,
            structure_indices=structure_indices,
            structure_indices_2=structure_indices_2,
            threshold=distance_threshold,
            pbc=pbc,
            output_type="csr",
        )

    if molecular_system_2 is None:
        if acceptors is None:
            acceptors = get_acceptor_atoms(
                molecular_system, selection=selection, syntax=syntax
            )
        else:
            acceptors = select(
                molecular_system, selection=selection, mask=acceptors, syntax=syntax
            )

        if donors is None:
            donors = get_donor_atoms(
                molecular_system, selection=selection, syntax=syntax
            )
        else:
            donors = select(
                molecular_system, selection=selection, mask=donors, syntax=syntax
            )

        n_donors = donors.shape[0]

        if (selection_2 is None) and (acceptors_2 is None) and (donors_2 is None):
            if n_donors == 0 or len(acceptors) == 0:
                return deliver(
                    empty_result(molecular_system, structure_indices), donors, acceptors
                )

        if (selection_2 is None) and (acceptors_2 is None) and (donors_2 is None):
            offsets, indices, distances = neighbors(donors[:, 1], acceptors)

            output_atoms = []
            output_distances = []

            n_structures = (len(offsets) - 1) // n_donors
            for structure_index in range(n_structures):
                tmp_atoms = []
                tmp_distances = []
                for ii in range(n_donors):
                    atom_d = donors[ii, 0]
                    atom_h = donors[ii, 1]
                    w = structure_index * n_donors + ii
                    for p in range(offsets[w], offsets[w + 1]):
                        jj = indices[p]
                        if atom_d != acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(distances[p])
                output_atoms.append(np.array(tmp_atoms))
                output_distances.append(
                    puw.utils.sequences.concatenate(
                        tmp_distances, value_type="numpy.ndarray"
                    )
                    if tmp_distances
                    else puw.quantity(np.empty(0), "nanometers")
                )

            return deliver(
                pack_result(output_atoms, output_distances), donors, acceptors
            )

        else:
            if selection_2 is None:
                selection_2 = selection

            if acceptors_2 is None:
                acceptors_2 = get_acceptor_atoms(
                    molecular_system, selection=selection_2, syntax=syntax
                )
            else:
                acceptors_2 = select(
                    molecular_system,
                    selection=selection_2,
                    mask=acceptors_2,
                    syntax=syntax,
                )

            if donors_2 is None:
                donors_2 = get_donor_atoms(
                    molecular_system, selection=selection_2, syntax=syntax
                )
            else:
                donors_2 = select(
                    molecular_system,
                    selection=selection_2,
                    mask=donors_2,
                    syntax=syntax,
                )

            n_donors_2 = donors_2.shape[0]

            offsets, indices, distances = neighbors(donors[:, 1], acceptors_2)
            offsets_2, indices_2, distances_2 = neighbors(donors_2[:, 1], acceptors)

            output_atoms = []
            output_distances = []

            if n_donors:
                n_structures = (len(offsets) - 1) // n_donors
            elif n_donors_2:
                n_structures = (len(offsets_2) - 1) // n_donors_2
            else:
                return deliver(
                    empty_result(molecular_system, structure_indices),
                    donors,
                    acceptors,
                    donors_2,
                    acceptors_2,
                )
            for structure_index in range(n_structures):
                tmp_atoms = []
                tmp_distances = []

                for ii in range(n_donors):
                    atom_d = donors[ii, 0]
                    atom_h = donors[ii, 1]
                    w = structure_index * n_donors + ii
                    for p in range(offsets[w], offsets[w + 1]):
                        jj = indices[p]
                        if atom_d != acceptors_2[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors_2[jj]])
                            tmp_distances.append(distances[p])

                for ii in range(n_donors_2):
                    atom_d = donors_2[ii, 0]
                    atom_h = donors_2[ii, 1]
                    w = structure_index * n_donors_2 + ii
                    for p in range(offsets_2[w], offsets_2[w + 1]):
                        jj = indices_2[p]
                        if atom_d != acceptors[jj]:
                            tmp_atoms.append([atom_d, atom_h, acceptors[jj]])
                            tmp_distances.append(distances_2[p])

                output_atoms.append(np.array(tmp_atoms))
                output_distances.append(
                    puw.utils.sequences.concatenate(
                        tmp_distances, value_type="numpy.ndarray"
                    )
                    if tmp_distances
                    else puw.quantity(np.empty(0), "nanometers")
                )

            return deliver(
                pack_result(output_atoms, output_distances),
                donors,
                acceptors,
                donors_2,
                acceptors_2,
            )

    raise NotImplementedMethodError(
        caller="molsysmt.interactions.hbonds.get_buch_hbonds"
    )
