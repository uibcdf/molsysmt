from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
import numpy as np
from smonitor import signal

from molsysmt.configure import with_configure_overrides

@signal(tags=['api', 'structure'])
@with_configure_overrides
@arg_digest()
def least_rmsd_align(molecular_system, selection='atom_name=="CA"', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          syntax='MolSysMT', engine_sequence_alignment = 'Biopython', engine_least_rmsd_fit = 'MolSysMT',
          in_place=False, use_gpu=None, gpu_backend=None, precision=None, skip_digestion=False):

    """
    Align a molecular system to a reference using sequence alignment followed by least-RMSD fitting.

    This is a two-step procedure:

    1. **Sequence alignment** — the topology of both systems is aligned using
       ``molsysmt.topology.get_sequence_identity`` (via ``engine_sequence_alignment``)
       to identify structurally equivalent residue groups.
    2. **Least-RMSD fit** — ``least_rmsd_fit`` is called on the equivalent atoms
       to compute the optimal rotation/translation (Kabsch algorithm) and apply it
       to all atoms in the selected components.

    This function is suitable for aligning homologous proteins whose sequences
    differ, where a simple atom-by-atom correspondence cannot be assumed.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='atom_name=="CA"'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    reference_molecular_system : molecular system or None, default=None
        Reference molecular system; `None` uses the input molecular system.
    reference_selection : str, list, tuple, or numpy.ndarray, or None, default=None
        Atoms selected from the reference molecular system.
    reference_structure_index : int, default=0
        Zero-based structure index selected from the reference system.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine_sequence_alignment : str, default='Biopython'
        Backend used to align the reference and target sequences.
    engine_least_rmsd_fit : str, default='MolSysMT'
        Backend used for the least-RMSD fit.
    in_place : bool, default=False
        Whether to modify the input molecular system in place.
    use_gpu : bool, default=None
        Whether to perform computation using GPU acceleration.
    gpu_backend : str or None, default=None
        GPU array backend, or `None` to use the configured backend.
    precision : {'single', 'double'} or None, default=None
        Floating-point precision, or `None` to use the configured precision.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or None
        A new molecular system with the aligned coordinates when
        ``in_place=False``; ``None`` when ``in_place=True``.


    Raises
    ------
    NotImplementedMethodError
        If an unsupported sequence-alignment engine or least-RMSD-fit engine is
        requested.


    .. versionadded:: 1.0.0
    """

    output = None

    if reference_selection is None:
        reference_selection = selection

    from molsysmt.basic import select

    if engine_sequence_alignment == 'Biopython':

        from molsysmt.topology import get_sequence_identity

        identity, identical_groups, reference_identical_groups = get_sequence_identity(molecular_system,
                selection=selection, reference_molecular_system=reference_molecular_system, reference_selection=reference_selection,
                engine='Biopython')

    else:

        raise NotImplementedMethodError(caller='molsysmt.structure.least_rmsd_align')

    aux_atoms_list = select(molecular_system, element='atom',
            selection='group_index==@identical_groups')
    selection_to_be_fitted = select(molecular_system, element='atom', selection=selection,
            mask=aux_atoms_list)
    components_selected = select(molecular_system, element='component', selection=selection)
    atoms_in_components_selected = select(molecular_system, element='atom', selection='component_index==@components_selected')

    aux_atoms_list = select(reference_molecular_system, element='atom', selection='group_index==@reference_identical_groups')
    reference_selection_to_be_fitted = select(reference_molecular_system, element='atom',
            selection=reference_selection, mask=aux_atoms_list)

    del(aux_atoms_list, components_selected)
    del(identity, identical_groups, reference_identical_groups)

    if engine_least_rmsd_fit == 'MolSysMT':

        from molsysmt.structure import least_rmsd_fit

        if in_place:

            least_rmsd_fit(molecular_system=molecular_system, selection=atoms_in_components_selected,
                    selection_fit=selection_to_be_fitted,
                    structure_indices=structure_indices, reference_molecular_system=reference_molecular_system,
                    reference_selection_fit=reference_selection_to_be_fitted,
                    reference_structure_index=reference_structure_index,
                    to_form=None, in_place=in_place, engine='MolSysMT', syntax=syntax,
                    use_gpu=use_gpu, gpu_backend=gpu_backend, precision=precision, skip_digestion=True)

            del(atoms_in_components_selected, selection_to_be_fitted, reference_selection_to_be_fitted)
            del(structure_indices, reference_structure_index)


        else:

            output = least_rmsd_fit(molecular_system=molecular_system, selection=atoms_in_components_selected,
                    selection_fit=selection_to_be_fitted,
                    structure_indices=structure_indices, reference_molecular_system=reference_molecular_system,
                    reference_selection_fit=reference_selection_to_be_fitted,
                                    reference_structure_index=reference_structure_index,
                    to_form=None, in_place=in_place, engine='MolSysMT', syntax=syntax,
                    use_gpu=use_gpu, gpu_backend=gpu_backend, precision=precision, skip_digestion=True)

            del(atoms_in_components_selected, selection_to_be_fitted, reference_selection_to_be_fitted)
            del(structure_indices, reference_structure_index)


            return output

    else:

        raise NotImplementedMethodError(caller='molsysmt.structure.least_rmsd_align')

