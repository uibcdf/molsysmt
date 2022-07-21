from molsysmt._private.exceptions.not_implemented import NotImplementedError
from molsysmt._private.digestion import *

@digest
def get_non_standard_residues(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        temp_molecular_system.findNonstandardResidues()

        for group, substitution in tmp_item.nonstandardResidues:
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=substitution.name

    else:

        raise NotImplementedError

    return output

