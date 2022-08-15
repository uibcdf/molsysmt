from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import *

@digest()
def get_missing_residues(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        temp_molecular_system.findMissingResidues()

        for group, substitution in temp_molecular_system.missingResidues:
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=substitution.name

    else:

        raise NotImplementedMethodError

    return output

