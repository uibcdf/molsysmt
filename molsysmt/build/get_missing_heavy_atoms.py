from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def get_missing_heavy_atoms(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntax = digest_syntax(syntax)
        selection = digest_selection(selection, syntax)
        engine = digest_engine(engine)

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, check=False)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()

        for group, atoms in temp_molecular_system.missingAtoms.items():
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=[]
            for atom in atoms:
                output[original_group_index].append(atom.name)

    else:

        raise NotImplementedError


    return output

