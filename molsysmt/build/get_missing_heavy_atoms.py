from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools._digestion import digest_engine
from molsysmt.basic import convert, get_form

def get_missing_heavy_atoms(molecular_system, selection='all', engine='PDBFixer',
                            syntaxis='MolSysMT'):

    engine = digest_engine(engine)

    output = None

    if engine=="PDBFixer":

        tmp_item = convert(molecular_system, selection=selection, to_form="pdbfixer.PDBFixer",
                           syntaxis=syntaxis)

        tmp_item.findMissingAtoms()
        output = tmp_item.missingAtoms

    else:

        raise NotImplementedError


    return output

