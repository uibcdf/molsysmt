from molsysmt._private.argdigest import arg_digest
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
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    center_of_atoms : bool, default=False
        Whether to compute distances relative to geometric centers.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    as_entity : object, default=True
        Argument as_entity.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    molecular_system_2 : object, default=None
        Argument molecular_system_2.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    center_of_atoms_2 : bool, default=False
        Whether to compute distances relative to geometric centers for selection_2.
    weights_2 : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for selection_2.
    as_entity_2 : object, default=True
        Argument as_entity_2.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    pairs : object, default=False
        Argument pairs.
    pbc : bool, default=False
        Whether to take periodic boundary conditions into account.
    engine : object, default='MolSysMT'
        Argument engine.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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

