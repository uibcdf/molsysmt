from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def get_missing_terminal_cappings(molecular_system, selection='all', syntaxis='MolSysMT', engine='PDBFixer', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        engine = digest_engine(engine)

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, check=False)

        temp_molecular_system = convert(molecular_system, selection=selection, to_form="pdbfixer.PDBFixer", syntaxis=syntaxis, check=False)

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        missingAtoms = tmp_item.missingTerminals

        for group, atoms in temp_molecular_system.missingTerminals.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=atoms

    else:

        raise NotImplementedError

    return output

