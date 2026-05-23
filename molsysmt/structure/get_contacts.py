from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_iterable_of_pairs
from molsysmt import pyunitwizard as puw
from molsysmt.configure import with_configure_overrides
import numpy as np
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
@with_configure_overrides
def get_contacts(molecular_system, selection=None, center_of_atoms=False, weights=None, structure_indices="all",
                 selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
                 threshold='12 angstroms', pairs=False, pbc=True, syntax='MolSysMT',
                 output_type='numpy.ndarray', output_indices=None, use_gpu=None, gpu_backend=None, skip_digestion=False):

    """
    Compute a boolean contact map between two sets of atoms (or atom-group centers).

    Internally calls ``get_distances`` and applies a distance threshold to produce
    a contact map.  When only one selection is provided the contact map is computed
    between all pairs within that selection.  When both ``selection`` and
    ``selection_2`` are provided the map is computed between the two sets.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, optional
        First set of atoms (or atom-group centroids when ``center_of_atoms=True``).
        Nested iterables are treated as groups of atoms.
    center_of_atoms : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection``
        instead of individual atom positions.
    weights : array-like, optional
        Per-atom weights for centroid computation of the first selection.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which contacts are evaluated.
    selection_2 : str, list, tuple or numpy.ndarray, optional
        Second set of atoms.  When ``None``, contacts are computed within
        ``selection`` itself.
    center_of_atoms_2 : bool, default False
        If ``True``, use the (weighted) centroid of each group in ``selection_2``.
    weights_2 : array-like, optional
        Per-atom weights for centroid computation of the second selection.
    structure_indices_2 : 'all', array-like or None, default None
        Frame indices for the second selection.  When ``None``, the same frames
        as ``structure_indices`` are used.
    threshold : str or quantity, default '12 angstroms'
        Distance cutoff for defining a contact.  Accepts any PyUnitWizard-parseable
        length quantity (e.g. ``'12 angstroms'``, ``puw.quantity(1.2, 'nm')``).
    pairs : bool, default False
        If ``True``, ``selection`` is interpreted as an array of pre-defined pairs
        and only the distance for each pair is evaluated (1-D output instead of 2-D).
    pbc : bool, default True
        Whether to apply periodic boundary conditions.  The actual PBC state is
        queried from the system; this flag disables the query when set to ``False``.
    syntax : str, default 'MolSysMT'
        Selection syntax used when selections are strings.
    output_type : {'numpy.ndarray', 'pairs', 'sorted pairs'}, default 'numpy.ndarray'
        Format of the returned contact map.

        * ``'numpy.ndarray'``: boolean array of shape
          ``(n_structures, n_elements_1)`` (pairs mode) or
          ``(n_structures, n_elements_1, n_elements_2)`` (matrix mode).
        * ``'pairs'`` / ``'sorted pairs'``: list of lists of contacting pair indices,
          one list per frame.
    output_indices : {None, 'selection', 'atom'}, default None
        Controls the index convention used when ``output_type`` is ``'pairs'``
        or ``'sorted pairs'``.

        * ``None``: raw positional indices into the distance array.
          ``'selection'``: positional indices within the selection arrays.
          ``'atom'``: global atom indices in the molecular system.
    use_gpu : bool or 'auto' or None, default None
        Whether to run calculation on GPU.
    gpu_backend : {'cuda', 'taichi'} or None, default None
        The preferred GPU framework to execute calculations on.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    numpy.ndarray or list
        Contact map as a boolean ``numpy.ndarray`` (``output_type='numpy.ndarray'``)
        or as a list of contacting pairs per frame (``output_type='pairs'`` or
        ``'sorted pairs'``).

    .. versionadded:: 1.0.0
    """

    from molsysmt.structure.get_distances import get_distances
    from molsysmt.basic import select, get
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    if pairs and (selection_2 is None):
        if is_iterable_of_pairs(selection):
            if not isinstance(selection, np.ndarray):
                selection=np.array(selection)
            selection_2 = selection[:,1]
            selection = selection[:,0]

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if selection_2 is None:
        atom_indices_2 = None
    else:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)

    # Check if GPU execution is requested and resolved
    from molsysmt._private.gpu import resolve_use_gpu
    import molsysmt.configure as config
    from molsysmt.lib.structure._kernel_inputs import (
        align_coordinates_values_and_unit,
        extract_coordinates_value_and_unit,
    )

    # 1. Fetch coordinates
    if center_of_atoms:
        from molsysmt.structure.get_center import get_center
        coordinates = get_center(molecular_system, selection=atom_indices,
                structure_indices=structure_indices, weights=weights)
    else:
        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)

    if atom_indices_2 is not None:
        if center_of_atoms_2:
            from molsysmt.structure.get_center import get_center
            coordinates_2 = get_center(molecular_system, selection=atom_indices_2,
                    structure_indices=structure_indices_2 or structure_indices, weights=weights_2)
        else:
            coordinates_2 = get(molecular_system, element='atom', selection=atom_indices_2,
                                structure_indices=structure_indices_2 or structure_indices, syntax=syntax,
                                coordinates=True)
    else:
        coordinates_2 = None

    # Calculate payload size
    coords_val, length_unit = extract_coordinates_value_and_unit(coordinates)
    if coordinates_2 is None:
        coords_2_val = None
        if pairs:
            payload = coords_val.shape[0] * coords_val.shape[1]
        else:
            payload = coords_val.shape[0] * coords_val.shape[1] * coords_val.shape[1]
    else:
        _, coords_2_val, _ = align_coordinates_values_and_unit(coordinates, coordinates_2)
        if pairs:
            payload = coords_val.shape[0] * coords_val.shape[1]
        else:
            payload = coords_val.shape[0] * coords_val.shape[1] * coords_2_val.shape[1]

    # Resolve GPU execution
    _use_gpu = resolve_use_gpu(use_gpu, payload)

    # If GPU is resolved, choose the backend
    contact_map = None
    if _use_gpu:
        # Convert threshold value to length unit of coordinates
        threshold_val = puw.get_value(threshold, to_unit=length_unit)

        # Get box if pbc is requested
        box = None
        if pbc:
            box = get(molecular_system, element="system", structure_indices=structure_indices, box=True)
            if box is not None and box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
            else:
                box = None

        # Check if we should use Taichi Lang backend
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
                if pairs:
                    if coords_2_val is None:
                        coords_2_val = coords_val
                    if box is not None:
                        from molsysmt.lib.structure.get_contacts_taichi import get_mic_contacts_pairs as _kernel
                        contact_map = _kernel(coords_val, coords_2_val, box, threshold_val)
                    else:
                        from molsysmt.lib.structure.get_contacts_taichi import get_contacts_pairs as _kernel
                        contact_map = _kernel(coords_val, coords_2_val, threshold_val)
                elif coords_2_val is None:
                    if box is not None:
                        from molsysmt.lib.structure.get_contacts_taichi import get_mic_contacts_single_system as _kernel
                        contact_map = _kernel(coords_val, box, threshold_val)
                    else:
                        from molsysmt.lib.structure.get_contacts_taichi import get_contacts_single_system as _kernel
                        contact_map = _kernel(coords_val, threshold_val)
                else:
                    if box is not None:
                        from molsysmt.lib.structure.get_contacts_taichi import get_mic_contacts as _kernel
                        contact_map = _kernel(coords_val, coords_2_val, box, threshold_val)
                    else:
                        from molsysmt.lib.structure.get_contacts_taichi import get_contacts as _kernel
                        contact_map = _kernel(coords_val, coords_2_val, threshold_val)

        # Fallback/Default Numba CUDA backend
        if contact_map is None:
            if pairs:
                if coords_2_val is None:
                    coords_2_val = coords_val
                if box is not None:
                    from molsysmt.lib.structure.get_contacts_cuda import get_mic_contacts_pairs as _kernel
                    contact_map = _kernel(coords_val, coords_2_val, box, threshold_val)
                else:
                    from molsysmt.lib.structure.get_contacts_cuda import get_contacts_pairs as _kernel
                    contact_map = _kernel(coords_val, coords_2_val, threshold_val)
            elif coords_2_val is None:
                if box is not None:
                    from molsysmt.lib.structure.get_contacts_cuda import get_mic_contacts_single_system as _kernel
                    contact_map = _kernel(coords_val, box, threshold_val)
                else:
                    from molsysmt.lib.structure.get_contacts_cuda import get_contacts_single_system as _kernel
                    contact_map = _kernel(coords_val, threshold_val)
            else:
                if box is not None:
                    from molsysmt.lib.structure.get_contacts_cuda import get_mic_contacts as _kernel
                    contact_map = _kernel(coords_val, coords_2_val, box, threshold_val)
                else:
                    from molsysmt.lib.structure.get_contacts_cuda import get_contacts as _kernel
                    contact_map = _kernel(coords_val, coords_2_val, threshold_val)

    # Fallback to CPU pipeline if GPU was not used
    if contact_map is None:
        all_dists = get_distances(molecular_system=molecular_system, selection=atom_indices,
                    center_of_atoms=center_of_atoms, weights=weights, structure_indices=structure_indices,
                    selection_2=atom_indices_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                    structure_indices_2=structure_indices_2, pairs=pairs, pbc=pbc, skip_digestion=True)

        length_units = puw.get_unit(all_dists)
        threshold = puw.get_value(threshold, to_unit=length_units)
        all_dists = puw.get_value(all_dists)

        num_structures=all_dists.shape[0]
        contact_map=np.empty(all_dists.shape, dtype=bool)

        for indice_structure in range(num_structures):
            if pairs:
                contact_map[indice_structure,:]=(all_dists[indice_structure,:]<=threshold)
            else:
                contact_map[indice_structure,:,:]=(all_dists[indice_structure,:,:]<=threshold)

        del(all_dists, num_structures, indice_structure, length_units)
        gc.collect()

    output = None

    if output_type=='numpy.ndarray':

        output = contact_map

    elif output_type in ['pairs', 'sorted pairs']:

        output = []
        n_contact_maps = contact_map.shape[0]

        if pairs:

            if output_indices=='selection':
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii,:]==True)[0]
                    output.append(aux_pairs.tolist())
            elif output_indices=='atom':
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii,:]==True)[0]
                    output.append([[selection[ii],selection_2[ii]] for ii in aux_pairs])

        else:

            if selection_2 is None:
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(np.triu(contact_map[ii],k=1)==True)
                    aux_pairs = np.column_stack(aux_pairs).tolist()
                    output.append(aux_pairs)
            else:
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii])
                    aux_pairs = np.column_stack(aux_pairs).tolist()
                    output.append(aux_pairs)

            if output_indices=='atom':

                atom_indices = np.array(atom_indices)

                if atom_indices_2 is None:
                    for ii in range(n_contact_maps):
                        output[ii]=atom_indices[output[ii]].tolist()
                else:
                    atom_indices_2 = np.array(atom_indices_2)
                    for ii in range(n_contact_maps):
                        aux_pairs = np.array(output[ii])
                        output[ii]=np.column_stack([atom_indices[aux_pairs[:,0]],
                                atom_indices_2[aux_pairs[:,1]]]).tolist()

        if output_type=='sorted pairs':
            for ii in range(n_contact_maps):
                output[ii] = sorted(output[ii])

    return output



