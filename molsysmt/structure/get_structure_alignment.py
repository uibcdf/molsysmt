from molsysmt.basic import select
import numpy as np

def get_structure_alignment(molecular_system, selection_alignment='all', selection_rmsd='backbone',
        frame_indices='all', reference_molecular_system=None, reference_selection_alignment='all',
        reference_selection_rmsd=None, reference_frame_index=0, syntaxis='MolSysMT', parallel=True,
        engine_sequence_alignment = 'biopython', engine_least_rmsd_fit = 'MolSysMT'):

    from molsysmt.structure.least_rmsd_fit import least_rmsd_fit

    if reference_selection_rmsd is None:
        reference_selection_rmsd = selection_rmsd

    if engine_sequence_alignment == 'biopython':

        idty, mask_reference_molecular_system, mask_molecular_system = sequence_identity(molecular_system,
                selection=selection_alignment,
                reference_molecular_system=reference_molecular_system,
                reference_selection=reference_selection_alignment,
                target_intersection_set="atom", engine='biopython')

        molecular_system_selection = select(molecular_system, selection=selection_rmsd, mask=mask_molecular_system)
        reference_molecular_system_selection = select(reference_molecular_system, selection=reference_selection_rmsd, mask=mask_reference_molecular_system)

        return least_rmsd_fit(molecular_system=molecular_system, selection=molecular_system_selection, frame_indices=frame_indices,
                               reference_molecular_system=reference_molecular_system,
                               reference_selection=reference_molecular_system_selection,
                               reference_frame_index=reference_frame_index,
                               engine=engine_least_rmsd_fit, parallel=parallel, syntaxis=syntaxis)

    else:

        raise NotImplementedError

