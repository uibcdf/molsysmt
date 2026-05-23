from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
import numpy as np
import gc
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
        Query system to be aligned, in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'atom_name=="CA"'
        Atoms (typically C-alpha carbons) used for sequence alignment and fitting.
        The entire component(s) containing the selected atoms are translated and
        rotated.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices of the query system to align.
    reference_molecular_system : molecular system or None, default None
        Reference system.  When ``None``, ``molecular_system`` itself is used.
    reference_selection : str, list, tuple or numpy.ndarray or None, default None
        Atoms in the reference used for sequence alignment.  When ``None``, the
        same expression as ``selection`` is applied to the reference.
    reference_structure_index : int, default 0
        Single frame index in the reference system to align to.
    syntax : str, default 'MolSysMT'
        Selection syntax used for both selections.
    engine_sequence_alignment : {'Biopython'}, default 'Biopython'
        Backend used for pairwise sequence alignment.
    engine_least_rmsd_fit : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the Kabsch rotation / RMSD minimisation.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the aligned
        coordinates.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

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

            gc.collect()

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

            gc.collect()

            return output

    else:

        raise NotImplementedMethodError(caller='molsysmt.structure.least_rmsd_align')


