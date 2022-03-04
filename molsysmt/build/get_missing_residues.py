from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import digest_engine

def get_missing_residues(molecular_system, selection='all', engine='PDBFixer', syntaxis='MolSysMT'):

    engine = digest_engine(engine)

    output = {}

    if engine=="PDBFixer":

        #from molsysmt.basic import convert, get_form, select

        #correction_group_indices = False
        #if selection is not 'all':
        #    group_indices_in_selection = select(molecular_system, target='group', selection=selection)
        #    correction_group_indices = True

        #tmp_item = convert(molecular_system, selection=selection, to_form="pdbfixer.PDBFixer",
        #                   syntaxis=syntaxis)

        #tmp_item.findMissingResidues()

        raise NotImplementedError()

    else:

        raise NotImplementedError


    return output

