from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def get_missing_heavy_atoms(molecular_system, selection='all', engine='PDBFixer',
                            syntaxis='MolSysMT'):

    engine = digest_engine(engine)

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        correction_group_indices = False
        if selection is not 'all':
            group_indices_in_selection = select(molecular_system, element='group', selection=selection)
            correction_group_indices = True

        tmp_item = convert(molecular_system, selection=selection, to_form="pdbfixer.PDBFixer",
                           syntaxis=syntaxis)

        tmp_item.findMissingResidues()
        tmp_item.findMissingAtoms()
        missingAtoms = tmp_item.missingAtoms

        for group, atoms in missingAtoms.items():
            if correction_group_indices:
                group_index = group_indices_in_selection[group.index]
            else:
                group_index = group.index
            output[group_index]=[]
            for atom in atoms:
                output[group_index].append(atom.name)

    else:

        raise NotImplementedError


    return output

