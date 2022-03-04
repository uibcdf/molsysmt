from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
import numpy as np

def align(molecular_system, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection='backbone', reference_frame_index=0,
          syntaxis='MolSysMT', parallel=True, method='sequence alignment and least rmsd fit',
          engine_sequence_alignment = 'biopython', engine_least_rmsd_fit = 'MolSysMT'):

    output = None

    if method == 'sequence alignment and least rmsd fit':

        from molsysmt.basic import select

        if engine_sequence_alignment == 'biopython':

            from molsysmt.topology import get_sequence_identity

            identity, identical_groups, reference_identical_groups = get_sequence_identity(molecular_system,
                    selection=selection, reference_molecular_system=reference_molecular_system, reference_selection=reference_selection,
                    engine='biopython')

        else:

            raise NotImplementedError

        aux_atoms_list = select(molecular_system, target='atom', selection='group_index==@identical_groups')
        selection_to_be_fitted = select(molecular_system, target='atom', selection=selection, mask=aux_atoms_list)

        aux_atoms_list = select(reference_molecular_system, target='atom', selection='group_index==@reference_identical_groups')
        reference_selection_to_be_fitted = select(reference_molecular_system, target='atom',
                selection=reference_selection, mask=aux_atoms_list)

        if engine_least_rmsd_fit == 'MolSysMT':

            from molsysmt.structure import fit


            output = fit(molecular_system=molecular_system, selection=selection_to_be_fitted, structure_indices=structure_indices,
                         reference_molecular_system=reference_molecular_system,
                         reference_selection=reference_selection_to_be_fitted, reference_frame_index=reference_frame_index,
                         engine='MolSysMT', parallel=parallel, syntaxis=syntaxis)

    else:

        raise NotImplementedError

    return output
