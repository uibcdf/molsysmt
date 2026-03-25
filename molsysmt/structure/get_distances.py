from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt._private.variables import is_iterable_of_pairs
from molsysmt._private.execution import Reducer
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np
import gc
from smonitor import signal


class _DistancesReducer(Reducer):
    """
    Reducer for get_distances heavy path.

    Supports single-system, all-vs-all atom distances per frame.
    PBC is applied per chunk when box is provided.
    Accumulates (chunk_size, n_atoms, n_atoms) arrays and concatenates on finalize,
    or writes directly into a PersistentResultHandle when output_handle is in metadata.
    """

    def __init__(self, pbc):
        self._pbc = pbc
        self._chunks = []
        self._output_handle = None
        self._frame_offset = 0

    def estimate_output_shape(self, metadata):
        """Use disk-backing only when the output would exceed the RAM budget."""
        import molsysmt.config as config
        n_structures = metadata['n_structures']
        n_atoms = metadata['n_atoms']
        output_bytes = n_structures * n_atoms * n_atoms * 8
        if output_bytes > config.max_ram_usage:
            return (n_structures, n_atoms, n_atoms)
        return None

    def initialize(self, metadata):
        self._chunks = []
        self._frame_offset = 0
        self._output_handle = metadata.get('output_handle')

    def consume(self, chunk):
        coords = np.array(chunk['coordinates'], dtype=np.float64)  # writable
        if self._pbc and chunk.get('box') is not None:
            box = np.array(chunk['box'], dtype=np.float64)
            result = msmlib.structure.get_mic_distances_single_system(coords, box)
        else:
            result = msmlib.structure.get_distances_single_system(coords)

        if self._output_handle is not None:
            n = result.shape[0]
            self._output_handle[self._frame_offset:self._frame_offset + n] = result
            self._frame_offset += n
        else:
            self._chunks.append(result)

    def finalize(self):
        if self._output_handle is not None:
            self._output_handle.flush()
            return self._output_handle
        return np.concatenate(self._chunks, axis=0)

    # --- optional extensions ---

    def checkpoint(self):
        if self._output_handle is not None:
            # Disk-backed: record frame offset only; the handle file persists on disk
            return {'frame_offset': self._frame_offset, 'disk_backed': True}
        return {'chunks': [c.tolist() for c in self._chunks], 'disk_backed': False}

    def restore(self, state):
        if state.get('disk_backed'):
            # Cannot reconnect to a PersistentResultHandle across process boundaries.
            # Resuming disk-backed reductions requires same-process continuation.
            raise NotImplementedError(
                "_DistancesReducer cannot restore a disk-backed checkpoint "
                "across separate process invocations."
            )
        self._chunks = [np.array(c, dtype=np.float64) for c in state['chunks']]
        self._frame_offset = 0
        self._output_handle = None

    def merge(self, other):
        if self._output_handle is not None or other._output_handle is not None:
            raise NotImplementedError(
                "_DistancesReducer.merge() is not supported with disk-backed output."
            )
        self._chunks.extend(other._chunks)


@signal(tags=['api', 'structure'])
@arg_digest()
def get_distances(molecular_system, selection="all", structure_indices="all", center_of_atoms=False, weights=None,
        molecular_system_2=None, selection_2=None, structure_indices_2=None, center_of_atoms_2=False, weights_2=None,
        pairs=False, pbc=True, output_type='numpy.ndarray', output_indices=None, output_structure_indices=None,
        engine='MolSysMT', syntax='MolSysMT', heavy_mode='auto', use_gpu=None, skip_digestion=False):
    """
    Computing distances between atoms or centers of selections.

    Parameters
    ----------
    molecular_system : molecular system
        First system (or the only one if `molecular_system_2` is None).
    selection, selection_2 : str, list, tuple or numpy.ndarray, default 'all'
        Atom selections for each system; if `pairs=True`, a list/array of index pairs is also accepted.
    structure_indices, structure_indices_2 : 'all' or array-like, default 'all'
        Structures/frames to analyze (0-based) for each system.
    center_of_atoms, center_of_atoms_2 : bool, default False
        If True, use centers of the selected atoms (weighted if `weights` provided).
    weights, weights_2 : array-like, optional
        Weights for centers when `center_of_atoms` is True.
    molecular_system_2 : molecular system, optional
        Second system; if None, distances are computed within `molecular_system`.
    pairs : bool, default False
        If True, interpret `selection` (or `selection`/`selection_2`) as explicit pairs.
    pbc : bool, default True
        Whether to consider periodic boundary conditions.
    output_type : {'numpy.ndarray', 'dictionary'}, default 'numpy.ndarray'
        Format of the returned distances.
    output_indices : {'selection', 'atom', 'group'}, optional
        When `output_type='dictionary'`, controls labeling of indices.
    output_structure_indices : {'structure'}, optional
        When `output_type='dictionary'`, controls labeling of structure indices.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend for the calculation.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    numpy.ndarray or dict
        Distances with shape `(n_structures, n_selection[, n_selection_2])` or structured dictionaries, depending on `output_type`.

    Raises
    ------
    NotImplementedMethodError
        If a requested path/output is not supported.

    Notes
    -----
    - Uses minimum image convention when `pbc=True` and box is available.
    - When `pairs=True`, expects explicit pairs; otherwise Cartesian products of selections are used.

    .. versionadded:: 1.0.0
    """

    # center_of_atoms and center_of_atoms_2: bool
    # output_type in ['numpy.ndarray','dictionary']

    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    if pairs and (selection_2 is None):
        if is_iterable_of_pairs(selection):
            if not isinstance(selection, np.ndarray):
                selection=np.array(selection)
            selection_2 = selection[:,1]
            selection = selection[:,0]
        elif len(selection)==2:
            selection_2 = selection[1]
            selection = selection[0]

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if molecular_system_2 is not None:
        if selection_2 is None:
            selection_2 = selection
        if structure_indices_2 is None:
            structure_indices_2 = structure_indices
        atom_indices_2 = select(molecular_system_2, selection=selection_2)
    else:
        if selection_2 is not None:
            atom_indices_2 = select(molecular_system, selection=selection_2)
        else:
            atom_indices_2 = None

    if is_iterable_of_iterables(atom_indices):
        center_of_atoms = True

    if is_iterable_of_iterables(atom_indices_2):
        center_of_atoms_2 = True

    if engine=='MolSysMT':

        from molsysmt.basic import get, get_form
        from molsysmt.form import is_file as _is_file

        in_memory = True
        if _is_file(get_form(molecular_system)):
            in_memory = False

        if in_memory:
            if molecular_system_2 is not None:
                if _is_file(get_form(molecular_system_2)):
                    in_memory = False

        # Decide eager vs heavy based on footprint
        from molsysmt._private.execution.memory_policy import estimate_footprint, decide_mode
        from molsysmt.basic import get_form, get as msm_get

        if is_all(atom_indices):
            _n_atoms_est = msm_get(molecular_system, element='system', n_atoms=True)
        else:
            _n_atoms_est = len(atom_indices)
        _n_structures_est = msm_get(molecular_system, element='system', n_structures=True)
        footprint = estimate_footprint(_n_atoms_est, _n_structures_est)
        mode = decide_mode(footprint, heavy_mode)

        heavy_eligible = (
            molecular_system_2 is None
            and not center_of_atoms
            and not pairs
            and not is_iterable_of_iterables(atom_indices)
        )

        if mode == 'heavy' and heavy_eligible:
            from molsysmt.form import _dict_modules
            form = get_form(molecular_system)
            form_module = _dict_modules.get(form)
            form_heavy = getattr(form_module, '_heavy_support', {})
            attrs = ['coordinates']
            if pbc and form_heavy.get('box', False):
                attrs.append('box')

            from molsysmt._private.execution import ChunkedExecutor
            reducer = _DistancesReducer(pbc=pbc and 'box' in attrs)
            executor = ChunkedExecutor(
                molecular_system=molecular_system,
                form=form,
                operation='get_distances',
                reducer=reducer,
                atom_indices=atom_indices,
                structure_indices=None if is_all(structure_indices) else structure_indices,
                heavy_mode=heavy_mode,
                attributes=attrs,
            )
            dist_val = executor.execute()  # (n_structures, n_atoms, n_atoms), float64, nm
            length_unit = puw.get_standard_units(dimensionality={'[L]': 1})
            distances = puw.quantity(dist_val, length_unit)

        else:

            distances = _get_distances_in_memory(molecular_system, selection=atom_indices,
                    structure_indices=structure_indices, center_of_atoms=center_of_atoms, weights=weights,
                    molecular_system_2=molecular_system_2, selection_2=atom_indices_2,
                    structure_indices_2=structure_indices_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                    pairs=pairs, pbc=pbc, syntax=syntax, use_gpu=use_gpu)

    else:

        raise NotImplementedMethodError


    if output_type=='numpy.ndarray':

        output_list = []

        if output_indices is not None:

            if pairs:

                raise NotImplementedMethodError(caller='molsysmt.structure.get_distances')

            else:

                if output_indices == 'selection': # works also with center of atoms

                    atom_indices = list(range(distances.shape[-2]))
                    output_list.append( atom_indices )

                    if atom_indices_2 is not None:

                        atom_indices_2 = list(range(distances.shape[-1]))
                        output_list.append( atom_indices_2 )

                elif output_indices == 'atom':

                    output_list.append( atom_indices )

                    if atom_indices_2 is not None:

                        output_list.append( atom_indices_2 )

                elif output_indices == 'group':

                    raise NotImplementedMethodError(caller='molsysmt.structure.get_distances')

        if output_structure_indices is not None:

            if output_structure_indices == 'selection':

                structure_indices = list(range(distances.shape[0]))
                output_list.append( structure_indices )

                if structure_indices_2 is not None:

                    structure_indices_2 = list(range(distances.shape[0]))
                    output_list.append( structure_indices_2 )

            elif output_structure_indices == 'structure':

                if is_all(structure_indices):
                    structure_indices = list(range(distances.shape[0]))
                    output_list.append( structure_indices )
                else:
                    output_list.append( structure_indices.tolist() )

                if structure_indices_2 is not None:
                    if is_all(structure_indices_2):
                        structure_indices_2 = list(range(distances.shape[0]))
                        output_list.append( structure_indices_2 )
                    else:
                        output_list.append( structure_indices_2.tolist() )

        output_list.append(distances)

        if len(output_list)==1:
            output = output_list[0]
        else:
            output = tuple(output_list)

    elif output_type=='dictionary':

        output_dictionary = {}

        if pairs:

            if output_indices is None:
                output_indices = 'atom'
            
            if output_indices is not None:

                if output_indices == 'selection': # works also with center of atoms
                    if output_structure_indices is None:
                        for ii in range(distances.shape[-1]):
                            output_dictionary[ii] = distances[:,ii]
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for ii in range(distances.shape[-1]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for ll,kk in enumerate(structure_indices):
                                    aux_ii[kk]=distances[ll,ii]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[1]))
                            for ii in range(distances.shape[-1]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for ll,kk in enumerate(structure_indices):
                                    aux_ii[kk]={}
                                    aux_ii_kk = aux_ii[kk]
                                    for mm,nn in enumerate(structure_indices_2):
                                        aux_ii_kk[nn]=distances[ll,mm,ii]

                elif output_indices == 'atom':
                    if output_structure_indices is None:
                        for aa,xx in enumerate(zip(atom_indices, atom_indices_2)):
                            if xx[0] not in output_dictionary:
                                output_dictionary[xx[0]] = {}
                            output_dictionary[xx[0]][xx[1]] = distances[:,aa]
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for aa,xx in enumerate(zip(atom_indices, atom_indices_2)):
                                if xx[0] not in output_dictionary:
                                    output_dictionary[xx[0]] = {}
                                if xx[1] not in output_dictionary[xx[0]]:
                                    output_dictionary[xx[0]][xx[1]] = {}
                                aux_0_1 = output_dictionary[xx[0]][xx[1]]
                                for ll,kk in enumerate(structure_indices):
                                    aux_0_1[kk]=distances[ll,aa]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[1]))
                            for aa,xx in enumerate(zip(atom_indices, atom_indices_2)):
                                if xx[0] not in output_dictionary:
                                    output_dictionary[xx[0]] = {}
                                if xx[1] not in output_dictionary[xx[0]]:
                                    output_dictionary[xx[0]][xx[1]] = {}
                                aux_0_1 = output_dictionary[xx[0]][xx[1]]
                                for ll,kk in enumerate(structure_indices):
                                    aux_0_1[kk]={}
                                    aux_0_1_kk=aux_0_1[kk]
                                    for mm,nn in enumerate(structure_indices_2):
                                        aux_0_1_kk[nn]=distances[ll,mm,aa]

                elif output_indices == 'group':

                    raise NotImplementedMethodError(caller='molsysmt.structure.get_distances')

        else:

            if output_indices is None:
                output_indices = 'atom'
            
            if output_indices is not None:

                if output_indices == 'selection': # works also with center of atoms
                    if output_structure_indices is None:
                        for ii in range(distances.shape[-2]):
                            output_dictionary[ii] = {jj:distances[:,ii,jj] for jj in range(distances.shape[-1])}
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for ii in range(distances.shape[-2]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for jj in range(distances.shape[-1]):
                                    aux_ii[jj] = {}
                                    aux_ii_jj = aux_ii[jj]
                                    for ll,kk in enumerate(structure_indices):
                                        kk = ll
                                        aux_ii_jj[kk]=distances[ll,ii,jj]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[0]))
                            for ii in range(distances.shape[-2]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for jj in range(distances.shape[-1]):
                                    aux_ii[jj] = {}
                                    aux_ii_jj = aux_ii[jj]
                                    for ll,kk in enumerate(structure_indices):
                                        nn = ll
                                        kk = ll
                                        aux_ii_jj[kk]={}
                                        aux_ii_jj_kk = aux_ii_jj[kk]
                                        aux_ii_jj_kk[nn]=distances[ll,ii,jj]

                elif output_indices == 'atom':
                    if output_structure_indices is None:
                        for aa,ii in enumerate(atom_indices):
                            output_dictionary[ii] = {}
                            aux_ii = output_dictionary[ii]
                            if atom_indices_2 is None:
                                for bb,jj in enumerate(atom_indices):
                                    aux_ii[jj] = distances[:,aa,bb]
                            else:
                                for bb,jj in enumerate(atom_indices_2):
                                    aux_ii[jj] = distances[:,aa,bb]
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for aa,ii in enumerate(atom_indices):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                if atom_indices_2 is None:
                                    for bb,jj in enumerate(atom_indices):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            aux_ii_jj[kk]=distances[ll,aa,bb]
                                else:
                                    for bb,jj in enumerate(atom_indices_2):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            aux_ii_jj[kk]=distances[ll,aa,bb]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[1]))
                            for aa,ii in enumerate(atom_indices):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                if atom_indices_2 is None:
                                    for bb,jj in enumerate(atom_indices):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            aux_ii_jj[kk]=distances[ll,aa,bb]
                                else:
                                    for bb,jj in enumerate(atom_indices_2):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            nn=structure_indices_2[ll]
                                            aux_ii_jj[kk] = {}
                                            aux_ii_jj_kk=aux_ii_jj[kk]
                                            aux_ii_jj_kk[nn]=distances[ll,aa,bb]

                elif output_indices == 'group':

                    raise NotImplementedMethodError(caller='molsysmt.structure.get_distances')

        output = output_dictionary

    return output


def _get_distances_in_memory(molecular_system, selection="all", structure_indices="all",
        center_of_atoms=False, weights=None,
        molecular_system_2=None, selection_2=None, structure_indices_2=None,
        center_of_atoms_2=False, weights_2=None,
        pairs=False, pbc=True, syntax='MolSysMT', use_gpu=None):
    """Internal helper to compute distances entirely in memory (no file-backed forms)."""

    from molsysmt.basic import get
    from .get_center import get_center
    from molsysmt.lib.structure._kernel_inputs import (
        align_coordinates_values_and_unit,
        extract_coordinates_value_and_unit,
    )

    if center_of_atoms:

        coordinates = get_center(molecular_system, selection=selection,
                structure_indices=structure_indices, weights=weights)

    else:

        coordinates = get(molecular_system, element='atom', selection=selection,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)

    if center_of_atoms_2:

        if molecular_system_2 is None:

            molecular_system_2 = molecular_system

        if structure_indices_2 is None:

            structure_indices_2 = structure_indices

        coordinates_2 = get_center(molecular_system_2, selection=selection_2,
            structure_indices=structure_indices_2, weights=weights_2)

    else:

        if (selection_2 is None) and (structure_indices_2 is None):

            if molecular_system_2 is None:

                coordinates_2 = None

            else:

                structure_indices_2 = structure_indices
                selection_2 = selection

                coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                                    structure_indices=structure_indices_2, syntax=syntax,
                                    coordinates=True)

        else:

            if structure_indices_2 is None:

                structure_indices_2 = structure_indices

            if selection_2 is None:

                selection_2 = selection

            if molecular_system_2 is None:

                molecular_system_2 = molecular_system

            coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                                structure_indices=structure_indices_2, syntax=syntax,
                                coordinates=True)


    from molsysmt._private.gpu import resolve_use_gpu

    if not pairs:

        if coordinates_2 is None:

            coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)
            payload = coordinates.shape[0] * coordinates.shape[1] * coordinates.shape[1]
            _use_gpu = resolve_use_gpu(use_gpu, payload)

            if pbc:
                box = get(molecular_system, element="system", structure_indices=structure_indices, box=True)
                if box is not None and box[0] is not None:
                    box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                    if _use_gpu:
                        from molsysmt.lib.structure.get_mic_distances_cuda import (
                            get_mic_distances_single_system as _gpu_mic_dist,
                        )
                        distances = _gpu_mic_dist(coordinates, box)
                    else:
                        distances = msmlib.structure.get_mic_distances_single_system(coordinates, box)
                elif _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances_single_system as _gpu_dist,
                    )
                    distances = _gpu_dist(coordinates)
                else:
                    distances = msmlib.structure.get_distances_single_system(coordinates)
            else:
                if _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances_single_system as _gpu_dist,
                    )
                    distances = _gpu_dist(coordinates)
                else:
                    distances = msmlib.structure.get_distances_single_system(coordinates)

        else:

            coordinates, coordinates_2, length_unit = align_coordinates_values_and_unit(
                coordinates, coordinates_2
            )
            payload = coordinates.shape[0] * coordinates.shape[1] * coordinates_2.shape[1]
            _use_gpu = resolve_use_gpu(use_gpu, payload)

            if pbc:
                box = get(molecular_system, element="system", structure_indices=structure_indices, box=True)
                if box is not None and box[0] is not None:
                    box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                    if _use_gpu:
                        from molsysmt.lib.structure.get_mic_distances_cuda import (
                            get_mic_distances as _gpu_mic_dist2,
                        )
                        distances = _gpu_mic_dist2(coordinates, coordinates_2, box)
                    else:
                        distances = msmlib.structure.get_mic_distances(coordinates, coordinates_2, box)
                elif _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances as _gpu_dist2,
                    )
                    distances = _gpu_dist2(coordinates, coordinates_2)
                else:
                    distances = msmlib.structure.get_distances(coordinates, coordinates_2)
            else:
                if _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances as _gpu_dist2,
                    )
                    distances = _gpu_dist2(coordinates, coordinates_2)
                else:
                    distances = msmlib.structure.get_distances(coordinates, coordinates_2)

    else: # pairs=True

        coordinates, coordinates_2, length_unit = align_coordinates_values_and_unit(
            coordinates, coordinates_2
        )

        if pbc:
            box = get(molecular_system, element="system", structure_indices=structure_indices, box=True)
            if box is not None and box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                distances = msmlib.structure.get_mic_distances_pairs(coordinates, coordinates_2, box)
            else:
                distances = msmlib.structure.get_distances_pairs(coordinates, coordinates_2)
        else:
            distances = msmlib.structure.get_distances_pairs(coordinates, coordinates_2)

    distances = puw.quantity(distances, length_unit)
    # We do NOT force standardize here to save time. 
    # The result is already in a coherent physical unit.


    gc.collect()

    return distances
