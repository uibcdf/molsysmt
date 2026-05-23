from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from smonitor import signal
from molsysmt import pyunitwizard as puw
from molsysmt.configure import with_configure_overrides
import numpy as np


@signal(tags=['api', 'physchem'])
@arg_digest()
@with_configure_overrides
def get_sasa(molecular_system, element='atom', selection='all', structure_indices='all',
             syntax='MolSysMT', engine='MolSysMT', use_gpu=None, gpu_backend=None, skip_digestion=False):
    """
    Solvent-accessible surface area (SASA) per atom or residue group.

    Uses the Shrake–Rupley rolling-sphere algorithm. The default engine
    computes SASA natively with optional GPU acceleration (Numba CUDA or Taichi).

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default 'atom'
        Hierarchical element over which SASA is accumulated.
        When ``element='atom'``, the raw per-atom SASA is returned.
        For any other element, per-atom values are summed within each element.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of elements to return.  The full system is always used for
        the SASA calculation; this parameter only filters the output.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MolSysMT', 'MDTraj'}, default 'MolSysMT'
        Backend used for the SASA calculation.
    use_gpu : bool or 'auto' or None, default None
        Whether to run calculation on GPU.
    gpu_backend : {'cuda', 'taichi'} or None, default None
        The preferred GPU framework to execute calculations on.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        SASA values as a PyUnitWizard quantity in area units (nm²).
        Shape: ``(n_structures, n_elements)``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    Notes
    -----
    Non-protein atoms (e.g. solvent) are included in the SASA calculation
    but their contribution to neighbouring atoms is accounted for.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import convert, select, get

    if engine == 'MDTraj':

        tmp_item = convert(molecular_system, to_form='mdtraj.Trajectory',
                           structure_indices=structure_indices)

        from mdtraj import shrake_rupley
        sasa_array = shrake_rupley(tmp_item, mode='atom')

        if element == 'atom':

            if not is_all(selection):
                atom_indices = select(molecular_system, selection=selection, syntax=syntax)
                sasa_array = sasa_array[:, atom_indices]

        else:

            sets_atoms = get(molecular_system, element=element, selection=selection,
                             syntax=syntax, atom_index=True)

            n_sets = len(sets_atoms)
            n_structures = sasa_array.shape[0]

            new_sasa_array = np.empty([n_structures, n_sets], dtype='float')
            for ii in range(n_sets):
                new_sasa_array[:, ii] = sasa_array[:, sets_atoms[ii]].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = puw.quantity(sasa_array, 'nm**2')
        sasa_array = puw.standardize(sasa_array)

    elif engine == 'MolSysMT':

        from molsysmt.physchem import get_atomic_radius
        from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
        from molsysmt._private.gpu import resolve_use_gpu
        import molsysmt.configure as config

        # Shrake-Rupley requires the full system to calculate occlusion correctly
        coordinates = get(molecular_system, element='atom', selection='all',
                          structure_indices=structure_indices, coordinates=True)
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        radii = get_atomic_radius(molecular_system, element='atom', selection='all', definition='vdw')
        radii_val = puw.get_value(radii, to_unit=length_unit)

        # 1.4 angstroms probe radius
        probe_radius = puw.get_value(puw.quantity(1.4, 'angstroms'), to_unit=length_unit)

        payload = coordinates.shape[0] * coordinates.shape[1]
        _use_gpu = resolve_use_gpu(use_gpu, payload)

        sasa_array = None

        if _use_gpu:
            box = None
            from molsysmt.pbc import has_pbc as _has_pbc
            if _has_pbc(molecular_system):
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None and box[0] is not None:
                    box = np.asarray(puw.get_value(box, to_unit=length_unit), dtype=np.float64)
                else:
                    box = None

            # Taichi backend
            if config.gpu_backend == 'taichi':
                try:
                    import taichi
                    taichi_available = True
                except ImportError:
                    taichi_available = False
                    import warnings
                    from molsysmt._private.smonitor import GpuNotAvailableWarning
                    warnings.warn(
                        "taichi package not found. Falling back to Numba CUDA backend.",
                        GpuNotAvailableWarning
                    )

                if taichi_available:
                    if box is not None:
                        from molsysmt.lib.structure.get_sasa_taichi import get_mic_sasa as _kernel
                        sasa_array = _kernel(coordinates, box, radii_val, probe_radius)
                    else:
                        from molsysmt.lib.structure.get_sasa_taichi import get_sasa as _kernel
                        sasa_array = _kernel(coordinates, radii_val, probe_radius)

            # Numba CUDA backend
            if sasa_array is None:
                if box is not None:
                    from molsysmt.lib.structure.get_sasa_cuda import get_mic_sasa as _kernel
                    sasa_array = _kernel(coordinates, box, radii_val, probe_radius)
                else:
                    from molsysmt.lib.structure.get_sasa_cuda import get_sasa as _kernel
                    sasa_array = _kernel(coordinates, radii_val, probe_radius)

        # Fallback to JIT CPU backend
        if sasa_array is None:
            box = None
            from molsysmt.pbc import has_pbc as _has_pbc
            if _has_pbc(molecular_system):
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None and box[0] is not None:
                    box = np.asarray(puw.get_value(box, to_unit=length_unit), dtype=np.float64)
                else:
                    box = None

            from molsysmt import lib as msmlib
            from molsysmt.lib.structure.get_sasa_cuda import get_fibonacci_sphere_points
            sphere_pts = get_fibonacci_sphere_points(100)

            if box is not None:
                sasa_array = msmlib.structure.get_mic_sasa(coordinates, box, radii_val, sphere_pts, probe_radius)
            else:
                sasa_array = msmlib.structure.get_sasa(coordinates, radii_val, sphere_pts, probe_radius)

        # Filter and accumulate results based on selection
        if element == 'atom':
            if not is_all(selection):
                atom_indices = select(molecular_system, selection=selection, syntax=syntax)
                sasa_array = sasa_array[:, atom_indices]
        else:
            sets_atoms = get(molecular_system, element=element, selection=selection,
                             syntax=syntax, atom_index=True)
            n_sets = len(sets_atoms)
            n_structures = sasa_array.shape[0]
            new_sasa_array = np.empty([n_structures, n_sets], dtype='float')
            for ii in range(n_sets):
                new_sasa_array[:, ii] = sasa_array[:, sets_atoms[ii]].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = puw.quantity(sasa_array, 'nm**2')
        sasa_array = puw.standardize(sasa_array)

    else:

        raise NotImplementedMethodError()

    return sasa_array
