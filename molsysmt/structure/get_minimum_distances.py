from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentConflictError
import numpy as np
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def get_minimum_distances(molecular_system, selection="all", center_of_atoms=False, weights=None, as_entity=True,
        structure_indices="all", molecular_system_2=None, selection_2=None, center_of_atoms_2=False, weights_2=None,
        as_entity_2=True, structure_indices_2=None, pairs=False, pbc=False, engine='MolSysMT', syntax='MolSysMT',
        skip_digestion=False):
    """
    Find the minimum pairwise distances between two sets of atoms (or atom-group centers).

    Internally calls ``get_distances`` and then reduces the full distance matrix by
    selecting the minimum entry according to the ``as_entity`` / ``as_entity_2``
    flags.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        First set of atoms.  Nested iterables are treated as groups of atoms when
        ``center_of_atoms=True``.
    center_of_atoms : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection``
        instead of individual atom positions.
    weights : array-like, optional
        Per-atom weights for centroid computation of the first selection.
    as_entity : bool, default True
        If ``True``, reduce over the entire first set to yield a single minimum
        per frame.  If ``False``, return the minimum partner for each element in
        the first set.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which the computation is performed.
    molecular_system_2 : molecular system or None, default None
        Second system.  When ``None``, both selections are drawn from
        ``molecular_system``.
    selection_2 : str, list, tuple or numpy.ndarray or None, default None
        Second set of atoms.  When ``None``, the minimum is computed within the
        first selection.
    center_of_atoms_2 : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection_2``.
    weights_2 : array-like, optional
        Per-atom weights for centroid computation of the second selection.
    as_entity_2 : bool, default True
        If ``True``, reduce over the entire second set to yield a single minimum
        per frame.  If ``False``, return the minimum partner for each element in
        the second set.
    structure_indices_2 : 'all', array-like or None, default None
        Frame indices for the second system.  When ``None``, the same frames as
        ``structure_indices`` are used.
    pairs : bool, default False
        If ``True``, ``selection`` is interpreted as an array of pre-defined pairs
        and the minimum is found among those pairs only.  Requires both
        ``as_entity`` and ``as_entity_2`` to be ``True``.
    pbc : bool, default False
        Apply minimum-image convention for periodic boundary conditions.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for distance computation.
    syntax : str, default 'MolSysMT'
        Selection syntax used when selections are strings.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    pairs_indices : numpy.ndarray
        Indices of the element pair (within the selection arrays) that achieves
        the minimum distance.  Shape depends on the ``as_entity`` flags and
        whether ``pairs`` mode is active.
    dists : quantity
        PyUnitWizard length quantity of the corresponding minimum distances in the
        standard length unit (nm).

    Raises
    ------
    ArgumentConflictError
        If both ``as_entity`` and ``as_entity_2`` are ``False`` (use
        ``get_distances`` directly in that case), or if ``pairs=True`` with
        ``as_entity=False`` or ``as_entity_2=False``.

    .. versionadded:: 1.0.0
    """

    from . import get_distances

    all_dists = get_distances(molecular_system=molecular_system, selection=selection, center_of_atoms=center_of_atoms,
            weights=weights, structure_indices=structure_indices, molecular_system_2=molecular_system_2,
            selection_2=selection_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights,
            structure_indices_2=structure_indices_2, pairs=pairs, pbc=pbc, engine=engine, syntax=syntax,
            skip_digestion=True)

    if pairs is False:

        nstructures, nelements_1, nelements_2 = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity is True) and (as_entity_2 is True):

            pairs=np.empty((nstructures,2),dtype=int)
            dists=np.empty((nstructures),dtype=float)
            for indice_structure in range(nstructures):
                ii,jj = np.unravel_index(all_dists[indice_structure,:,:].argmin(), all_dists[indice_structure,:,:].shape)
                pairs[indice_structure,0] = ii
                pairs[indice_structure,1] = jj
                dists[indice_structure] = all_dists[indice_structure,ii,jj]

            del(all_dists)
            gc.collect()

            dists=dists*length_units

            return pairs, dists

        elif (as_entity is False) and (as_entity_2 is True):

            pairs=np.empty((nstructures, nelements_1), dtype=int)
            dists=np.empty((nstructures, nelements_1), dtype=float)
            for indice_structure in range(nstructures):
                for ii in range(nelements_1):
                    jj = all_dists[indice_structure,ii,:].argmin()
                    pairs[indice_structure,ii]=jj
                    dists[indice_structure,ii]=all_dists[indice_structure,ii,jj]

            del(all_dists)
            gc.collect()

            dists=dists*length_units

            return pairs, dists

        elif (as_entity is True) and (as_entity_2 is False):

            pairs=np.empty((nstructures, nelements_2), dtype=int)
            dists=np.empty((nstructures, nelements_2), dtype=float)
            for indice_structure in range(nstructures):
                for ii in range(nelements_2):
                    jj = all_dists[indice_structure,:,ii].argmin()
                    dists[indice_structure,ii]=all_dists[indice_structure,jj,ii]

            del(all_dists)
            gc.collect()

            dists=dists*length_units

            return pairs, dists

        else:
            raise ArgumentConflictError(
                arg1="as_entity",
                arg2="as_entity_2",
                reason="If both input arguments 'as_entity' and 'as_entity_2' are False, the method you are looking for is molsysmt.distance()",
                caller="molsysmt.structure.get_minimum_distances"
            )

    else:

        nstructures, nelements = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity is True) and (as_entity_2 is True):

            pairs=np.empty((nstructures),dtype=int)
            dists=np.empty((nstructures),dtype=float)
            for indice_structure in range(nstructures):
                ii = all_dists[indice_structure,:].argmin()
                pairs[indice_structure] = ii
                dists[indice_structure] = all_dists[indice_structure,ii]

            del(all_dists)
            gc.collect()

            dists=dists*length_units

            return pairs, dists

        else:
            raise ArgumentConflictError(
                arg1="pairs",
                arg2="as_entity",
                reason="If 'pairs=True' both input arguments 'as_entity' and 'as_entity_2' need to be True",
                caller="molsysmt.structure.get_minimum_distances"
            )

