from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import numpy as np

@digest()
def align(molecular_system, selection='atom_name=="CA"', structure_indices='all',
          reference_molecular_system=None, reference_selection='atom_name=="CA"', reference_structure_index=0,
          syntax='MolSysMT', method='sequence alignment and least rmsd fit',
          engine_sequence_alignment = 'Biopython', engine_least_rmsd_fit = 'MolSysMT'):

    output = None

    if method == 'sequence alignment and least rmsd fit':

        from molsysmt.basic import select

        if engine_sequence_alignment == 'Biopython':

            from molsysmt.topology import get_sequence_identity

            identity, identical_groups, reference_identical_groups = get_sequence_identity(molecular_system,
                    selection=selection, reference_molecular_system=reference_molecular_system, reference_selection=reference_selection,
                    engine='Biopython')

        else:

            raise NotImplementedMethodError

        aux_atoms_list = select(molecular_system, element='atom',
                selection='group_index==@identical_groups')
        selection_to_be_fitted = select(molecular_system, element='atom', selection=selection,
                mask=aux_atoms_list)

        aux_atoms_list = select(reference_molecular_system, element='atom', selection='group_index==@reference_identical_groups')
        reference_selection_to_be_fitted = select(reference_molecular_system, element='atom',
                selection=reference_selection, mask=aux_atoms_list)

        if engine_least_rmsd_fit == 'MolSysMT':

            from molsysmt.structure import fit


            output = fit(molecular_system=molecular_system, selection=selection_to_be_fitted, structure_indices=structure_indices,
                         reference_molecular_system=reference_molecular_system,
                         reference_selection=reference_selection_to_be_fitted,
                         reference_structure_index=reference_structure_index,
                         engine='MolSysMT', syntax=syntax)

    else:

        raise NotImplementedMethodError

    return output

