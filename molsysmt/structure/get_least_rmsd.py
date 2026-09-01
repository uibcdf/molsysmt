from molsysmt._private.smonitor import NotImplementedMethodError, StructuralInconsistencyError
from smonitor import signal
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import lib as msmlib
from molsysmt._private import rust_backend as _kernels
from molsysmt import pyunitwizard as puw
import numpy as np

from molsysmt.configure import with_configure_overrides

@signal(tags=['api', 'structure'])
@arg_digest()
@with_configure_overrides
def get_least_rmsd(molecular_system, selection='atom_type!="H"', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          syntax='MolSysMT', engine='MolSysMT', use_gpu=None, parallel=None, num_threads=None, skip_digestion=False):


    """
    Compute the least-RMSD (optimal superposition RMSD) between structures.

    Unlike ``get_rmsd``, this function finds the rotation that minimises the
    RMSD before measuring it.  The algorithm operates in nm and returns a
    quantity in the MolSysMT standard length unit.

    The function handles three broadcasting scenarios:

    * Many query structures vs. one reference — each query frame is aligned to
      the single reference frame.
    * One query structure vs. many reference frames — the single query is aligned
      to each reference frame.
    * Equal numbers of frames on both sides — frame-by-frame alignment.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='atom_type!="H"'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    reference_molecular_system : object, default=None
        Argument reference_molecular_system.
    reference_selection : object, default=None
        Argument reference_selection.
    reference_structure_index : object, default=0
        Argument reference_structure_index.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Argument engine.
    use_gpu : bool, default=None
        Whether to perform computation using GPU acceleration.
    parallel : object, default=None
        Argument parallel.
    num_threads : object, default=None
        Argument num_threads.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        PyUnitWizard length quantity of shape ``(n_structures,)`` containing the
        least-RMSD values in the standard length unit (nm).


    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If the number of atoms resolved by ``selection`` and ``reference_selection``
        differ.


    .. versionadded:: 1.0.0
    """

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_selection is None:
        reference_selection = selection

    if engine=='MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt.lib.structure._kernel_inputs import align_coordinates_values_and_unit

        coordinates = get(molecular_system, element='atom', selection=selection,
                structure_indices=structure_indices, syntax=syntax,
                coordinates=True)

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_coordinates = get(reference_molecular_system, element='atom', selection=reference_selection,
                structure_indices=reference_structure_index, syntax=syntax,
                coordinates=True)

        coordinates, reference_coordinates, length_unit = align_coordinates_values_and_unit(
            coordinates,
            reference_coordinates,
        )

        if coordinates.shape[1]!=reference_coordinates.shape[1]:
            raise StructuralInconsistencyError(
                reason="reference selection and selection needs to have the same number of atoms",
                caller="molsysmt.structure.get_least_rmsd"
            )

        from molsysmt._private.gpu import resolve_use_gpu

        payload = coordinates.shape[0] * coordinates.shape[1] * 3
        _use_gpu = resolve_use_gpu(use_gpu, payload)

        if _use_gpu:
            from molsysmt.lib.structure.get_least_rmsd_cuda import (
                get_least_rmsd as get_least_rmsd_cuda,
                get_least_rmsd_with_single_reference_structure as get_least_rmsd_with_single_ref_cuda
            )
            if coordinates.shape[0] == 1 and reference_coordinates.shape[0] > 1:
                rmsd_val = get_least_rmsd_with_single_ref_cuda(reference_coordinates, coordinates[0])
            elif coordinates.shape[0] > 1 and reference_coordinates.shape[0] == 1:
                rmsd_val = get_least_rmsd_with_single_ref_cuda(coordinates, reference_coordinates[0])
            else:
                rmsd_val = get_least_rmsd_cuda(coordinates, reference_coordinates)
        else:
            if coordinates.shape[0] == 1 and reference_coordinates.shape[0] > 1:
                rmsd_val = _kernels.get_least_rmsd_with_single_reference_structure(reference_coordinates, coordinates[0])
            elif coordinates.shape[0] > 1 and reference_coordinates.shape[0] == 1:
                rmsd_val = _kernels.get_least_rmsd_with_single_reference_structure(coordinates, reference_coordinates[0])
            else:
                rmsd_val = _kernels.get_least_rmsd(coordinates, reference_coordinates)


        rmsd_val = puw.quantity(rmsd_val, length_unit, standardized=True)

        del(coordinates, reference_coordinates, length_unit)

        return rmsd_val

    else:

        raise NotImplementedMethodError()
