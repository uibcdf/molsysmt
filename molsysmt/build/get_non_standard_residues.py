from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def get_non_standard_residues(molecular_system, selection='all', syntaxis='MolSysMT', engine='PDBFixer'):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        engine = digest_engine(engine)

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, check=False)

        temp_molecular_system = convert(molecular_system, selection=selection, to_form="pdbfixer.PDBFixer", syntaxis=syntaxis)

        temp_molecular_system.findNonstandardResidues()

        for group, substitution in tmp_item.nonstandardResidues:
                original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=substitution.name

    else:

        raise NotImplementedError

    return output

