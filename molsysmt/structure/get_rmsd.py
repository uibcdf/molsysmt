from molsysmt._private.smonitor import NotImplementedMethodError, StructuralInconsistencyError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt._private.execution import Reducer
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


class _RMSDReducer(Reducer):
    """
    Reducer for get_rmsd heavy path.

    Reference coordinates are a single frame (n_atoms, 3), float64, in nm.
    Accumulates per-chunk RMSD arrays and concatenates on finalize.
    """

    def __init__(self, reference_coordinates):
        # reference_coordinates: (n_atoms, 3), float64, nm
        self._ref = reference_coordinates
        self._chunks = []

    def initialize(self, metadata):
        self._chunks = []

    def consume(self, chunk):
        coords = np.array(chunk['coordinates'], dtype=np.float64)  # writable copy
        rmsd_chunk = msmlib.structure.get_rmsd_with_single_reference_structure(coords, self._ref)
        self._chunks.append(rmsd_chunk)

    def finalize(self):
        return np.concatenate(self._chunks, axis=0)

    # --- optional extensions ---

    def checkpoint(self):
        return {'chunks': [c.tolist() for c in self._chunks]}

    def restore(self, state):
        self._chunks = [np.array(c, dtype=np.float64) for c in state['chunks']]

    def merge(self, other):
        self._chunks.extend(other._chunks)


@signal(tags=['api', 'structure'])
@arg_digest()
def get_rmsd(molecular_system, selection='atom_type!="H"', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          syntax='MolSysMT', engine='MolSysMT', heavy_mode='auto'):
    """
    To be written soon...
    """

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system

    if reference_selection is None:
        reference_selection = selection

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt.lib.structure._kernel_inputs import align_coordinates_values_and_unit

        # Always load reference eagerly — it is a single frame
        reference_coordinates = get(reference_molecular_system, element='atom',
                selection=reference_selection,
                structure_indices=reference_structure_index, syntax=syntax,
                coordinates=True)

        # Validate atom counts before going heavy
        from molsysmt.basic import get as msm_get
        n_atoms_sel = len(select(molecular_system, selection=selection, syntax=syntax))
        n_atoms_ref = len(select(reference_molecular_system, selection=reference_selection, syntax=syntax))

        if n_atoms_sel != n_atoms_ref:
            raise StructuralInconsistencyError(
                reason=f"Selection ({n_atoms_sel} atoms) and reference ({n_atoms_ref} atoms) counts mismatch.",
                caller="molsysmt.structure.get_rmsd"
            )

        n_structures = get(molecular_system, element='system', n_structures=True)

        from molsysmt._private.execution.memory_policy import estimate_footprint, decide_mode
        from molsysmt.basic import get_form

        form = get_form(molecular_system)
        footprint = estimate_footprint(n_atoms_sel, n_structures)
        mode = decide_mode(footprint, heavy_mode)

        if mode == 'heavy':
            # Extract reference as float64 numpy array in canonical length unit (nm)
            ref_val, length_unit = puw.get_value_and_unit(reference_coordinates,
                                                           value_type='numpy.ndarray',
                                                           dtype=np.float64)
            # ref_val shape may be (1, n_atoms, 3) — squeeze to (n_atoms, 3)
            ref_val = np.squeeze(ref_val, axis=0) if ref_val.ndim == 3 else ref_val

            atom_indices = select(molecular_system, selection=selection, syntax=syntax)
            reducer = _RMSDReducer(reference_coordinates=ref_val)

            from molsysmt._private.execution import ChunkedExecutor
            executor = ChunkedExecutor(
                molecular_system=molecular_system,
                form=form,
                operation='get_rmsd',
                reducer=reducer,
                atom_indices=atom_indices,
                structure_indices=None if is_all(structure_indices) else structure_indices,
                heavy_mode=heavy_mode,
                attributes=['coordinates'],
            )
            rmsd_val = executor.execute()  # (n_structures,), float64, nm
            return puw.quantity(rmsd_val, length_unit)

        else:
            coordinates = get(molecular_system, element='atom', selection=selection,
                    structure_indices=structure_indices, syntax=syntax,
                    coordinates=True)

            coordinates, reference_coordinates, length_unit = align_coordinates_values_and_unit(
                coordinates, reference_coordinates
            )

            n_atoms = coordinates.shape[1]
            n_atoms_ref_check = reference_coordinates.shape[1]

            if n_atoms != n_atoms_ref_check:
                raise StructuralInconsistencyError(
                    reason=f"Selection ({n_atoms} atoms) and reference ({n_atoms_ref_check} atoms) counts mismatch.",
                    caller="molsysmt.structure.get_rmsd"
                )

            if reference_coordinates.shape[0] == 1:
                rmsd_val = msmlib.structure.get_rmsd_with_single_reference_structure(
                    coordinates, reference_coordinates[0])
            elif coordinates.shape[0] == 1:
                rmsd_val = msmlib.structure.get_rmsd_with_single_reference_structure(
                    reference_coordinates, coordinates[0])
            else:
                rmsd_val = msmlib.structure.get_rmsd(coordinates, reference_coordinates)

            rmsd_val = puw.quantity(rmsd_val, length_unit)

            del coordinates, reference_coordinates, length_unit
            gc.collect()

            return rmsd_val

    else:

        raise NotImplementedMethodError()
