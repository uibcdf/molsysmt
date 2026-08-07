from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
import numpy as np
from molsysmt import pyunitwizard as puw
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def move_away(molecular_system, selection='all', center_of_selection='all', weights=None, structure_indices=0,
              reference_molecular_system=None, reference_center_of_selection='all', reference_weights=None,
              reference_structure_indices=None, direction=None, distance='3 angstroms',
              in_place=False, syntax='MolSysMT', skip_digestion=False):
    """
    Translate a selection of atoms away from a reference center by a fixed distance.

    Two operating modes are available depending on whether ``direction`` is
    provided:

    * **Auto direction** (``direction=None``): the displacement direction is
      computed automatically as the unit vector pointing from the center of
      ``reference_center_of_selection`` to the center of ``center_of_selection``.
      The atoms in ``selection`` are then translated by ``distance`` along that
      direction.
    * **Explicit direction**: the selection is first centered on the reference
      center (via ``molsysmt.structure.center``), then translated by ``distance``
      along the supplied unit vector.  Only single-frame / single-group use is
      supported in this mode.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms that will be physically displaced.
    center_of_selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms whose center defines the starting point of the displacement vector
        (ignored when ``direction`` is provided).
    weights : array-like, optional
        Per-atom weights for computing the center of ``center_of_selection``.
    structure_indices : int or array-like, default 0
        Frame index (or indices) of the system to operate on.
    reference_molecular_system : molecular system or None, default None
        System that defines the reference center.  When ``None``,
        ``molecular_system`` itself is used.
    reference_center_of_selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms in the reference system whose center serves as the origin of the
        displacement direction.
    reference_weights : array-like, optional
        Per-atom weights for computing the reference center.
    reference_structure_indices : int, array-like or None, default None
        Frame indices for the reference system.  When ``None``, the same value as
        ``structure_indices`` is used.
    direction : array-like or None, default None
        Explicit unit displacement vector of shape ``(1, 3)``.  When ``None``, the
        direction is derived from the two centers.
    distance : str or quantity, default '3 angstroms'
        Distance by which the atoms are displaced.  Accepts any
        PyUnitWizard-parseable length quantity (e.g. ``'3 angstroms'``,
        ``puw.quantity(0.3, 'nm')``).
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the updated
        coordinates.
    syntax : str, default 'MolSysMT'
        Selection syntax used when selections are strings.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    molecular system or None
        A new molecular system with the displaced coordinates when
        ``in_place=False``; ``None`` when ``in_place=True``.

    Raises
    ------
    NotImplementedMethodError
        When called with an explicit ``direction`` and more than one frame or more
        than one group — not yet implemented for that case.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, set, select, copy
    from molsysmt.structure import get_center, center

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_structure_indices is None:
        reference_structure_indices = structure_indices

    coordinates_reference_center = get_center(reference_molecular_system, selection=reference_center_of_selection,
                                              structure_indices=reference_structure_indices,
                                              weights=reference_weights, syntax=syntax, skip_digestion=True)

    if direction is None:

        coordinates_center = get_center(molecular_system, selection=center_of_selection, weights=weights,
                                        structure_indices=structure_indices, syntax=syntax, skip_digestion=True)

        direction = puw.get_value(coordinates_center-coordinates_reference_center)

        if direction.shape[0]!=1 or direction.shape[1]!=1:

            raise NotImplementedMethodError(caller='molsysmt.structure.move_away')

        direction = direction[:,0,:]
        for ii in range(direction.shape[0]):
            direction[ii] = direction[ii]/np.linalg.norm(direction[ii])

        atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
        coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                          coordinates=True, skip_digestion=True)

        value, unit = puw.get_value_and_unit(distance)
        value = value * direction
        n_atoms = coordinates.shape[1]
        value = np.tile(value, (n_atoms,1))
        translation = puw.quantity(value, unit)
        coordinates+=translation

        if in_place:
            return set(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                       coordinates=coordinates, skip_digestion=True)
        else:
            tmp_molecular_system = copy(molecular_system)
            set(tmp_molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                coordinates=coordinates, skip_digestion=True)
            return tmp_molecular_system

    else:

        if in_place:

            center(molecular_system, selection=selection, center_of_selection=center_of_selection, weights=weights,
                  center_coordinates=coordinates_reference_center, in_place=True, skip_digestion=True)

            atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
            coordinates = get(molecular_system, element='atom', selection=atom_indices,
                              structure_indices=structure_indices, coordinates=True, skip_digestion=True)

            if direction.shape[0]!=1 or coordinates.shape[0]!=1:
                raise NotImplementedMethodError(caller='molsysmt.structure.move_away')

            value, unit = puw.get_value_and_unit(distance)
            value = value * direction
            n_atoms = coordinates.shape[1]
            value = np.tile(value, (n_atoms,1))
            translation = puw.quantity(value, unit)
            coordinates+=translation

            return set(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                       coordinates=coordinates, skip_digestion=True)

        else:

            tmp_molecular_system = center(molecular_system, selection=selection,
                                          center_of_selection=center_of_selection, weights=weights,
                                          center_coordinates=coordinates_reference_center,
                                          in_place=False, skip_digestion=True)

            atom_indices = select(tmp_molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
            coordinates = get(tmp_molecular_system, element='atom', selection=atom_indices,
                              structure_indices=structure_indices, coordinates=True, skip_digestion=True)

            if direction.shape[0]!=1 or coordinates.shape[0]!=1:
                raise NotImplementedMethodError(caller='molsysmt.structure.move_away')

            value, unit = puw.get_value_and_unit(distance)
            value = value * direction
            n_atoms = coordinates.shape[1]
            value = np.tile(value, (n_atoms,1))
            translation = puw.quantity(value, unit)
            coordinates+=translation

            set(tmp_molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                coordinates=coordinates, skip_digestion=True)

            return tmp_molecular_system

