from molsysmt._private.smonitor import NotImplementedMethodError, StructuralInconsistencyError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import gc

from molsysmt.configure import with_configure_overrides

@signal(tags=['api', 'structure'])
@with_configure_overrides
@arg_digest()
def least_rmsd_fit(molecular_system=None, selection='all', selection_fit='atom_type!="H"', structure_indices='all',
        reference_molecular_system=None, reference_selection_fit=None, reference_structure_index=0,
        to_form=None, in_place=False, syntax='MolSysMT', engine='MolSysMT', parallel=None, num_threads=None, skip_digestion=False):

    """
    Superpose a molecular system onto a reference using the Kabsch least-RMSD algorithm.

    The optimal rotation matrix and translation vector that minimise the RMSD
    between ``selection_fit`` atoms and their counterparts in the reference are
    computed via the Kabsch algorithm.  The resulting rigid-body transformation is
    then applied to the broader ``selection`` (which may include more atoms than
    ``selection_fit``).

    Parameters
    ----------
    molecular_system : molecular system
        System to be fitted, in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        All atoms that will be physically moved by the fitted transformation.
        This is usually a superset of ``selection_fit`` (e.g., all atoms in a
        chain, while fitting is done on C-alpha only).
    selection_fit : str, list, tuple or numpy.ndarray, default 'atom_type!="H"'
        Subset of atoms used to compute the optimal superposition (heavy atoms
        by default).  Must resolve to the same number of atoms as
        ``reference_selection_fit``.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices of the query system to fit.
    reference_molecular_system : molecular system or None, default None
        Reference system.  When ``None``, ``molecular_system`` itself is used.
    reference_selection_fit : str, list, tuple or numpy.ndarray or None, default None
        Atoms in the reference used to compute the superposition.  When ``None``,
        the same expression as ``selection_fit`` is applied to the reference.
    reference_structure_index : int, default 0
        Single frame index in the reference system to fit to.
    to_form : str or None, default None
        Convert the output to the specified MolSysMT form before returning.
        When ``None``, the same form as the input is kept.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the fitted
        coordinates.
    syntax : str, default 'MolSysMT'
        Selection syntax used for all selections.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the Kabsch rotation computation.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    molecular system or None
        A new molecular system with the fitted coordinates (optionally converted
        to ``to_form``) when ``in_place=False``; ``None`` when ``in_place=True``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If the number of atoms resolved by ``selection_fit`` and
        ``reference_selection_fit`` differ.

    .. versionadded:: 1.0.0
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, copy, convert
        from molsysmt.lib.structure._kernel_inputs import align_coordinates_values_and_unit
        from . import rotate, translate

        coordinates = get(molecular_system, element='atom', selection=selection_fit,
                structure_indices=structure_indices, syntax=syntax, coordinates=True)

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection_fit is None:
            reference_selection_fit = selection_fit

        reference_coordinates = get(reference_molecular_system, element='atom',
                selection=reference_selection_fit, structure_indices=reference_structure_index,
                syntax=syntax, coordinates=True)

        coordinates, reference_coordinates, length_unit = align_coordinates_values_and_unit(
            coordinates,
            reference_coordinates,
        )

        if coordinates.shape[1]!=reference_coordinates.shape[1]:
            raise StructuralInconsistencyError(
                reason="reference selection and selection needs to have the same number of atoms",
                caller="molsysmt.structure.least_rmsd_fit"
            )

        if coordinates.shape[0]==1 and reference_coordinates.shape[0]>1:
            rotation_center, rotation, translation = \
                    msmlib.structure.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
                        reference_coordinates, coordinates[0])
        elif coordinates.shape[0]>1 and reference_coordinates.shape[0]==1:
            rotation_center, rotation, translation = \
                    msmlib.structure.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
                        coordinates, reference_coordinates[0])
        else:
            rotation_center, rotation, translation = msmlib.structure.get_least_rmsd_rotation_and_translation(
                coordinates, reference_coordinates)

        rotation_center = puw.quantity(rotation_center, length_unit, standardized=True)
        translation = puw.quantity(translation, length_unit, standardized=True)

        del(coordinates, reference_coordinates)

        if in_place:

            rotate(molecular_system, rotation=rotation, rotation_center=rotation_center,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            translate(molecular_system, translation=translation,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            del(rotation, rotation_center, translation)
            gc.collect()

        else:

            tmp_molecular_system = copy(molecular_system)

            rotate(tmp_molecular_system, rotation=rotation, rotation_center=rotation_center,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            translate(tmp_molecular_system, translation=translation,
                   selection=selection, structure_indices=structure_indices,
                   syntax=syntax, in_place=True)

            del(rotation, rotation_center, translation)
            gc.collect()

            if to_form is None:
                return tmp_molecular_system
            else:
                tmp_molecular_system = convert(tmp_molecular_system, to_form=to_form)
                return tmp_molecular_system

    else:

        raise NotImplementedMethodError()
