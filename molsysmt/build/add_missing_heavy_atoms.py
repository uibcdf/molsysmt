from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add_missing_heavy_atoms(molecular_system, selection='all', syntaxis='MolSysMT', engine='PDBFixer', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        engine = digest_engine(engine)

    from molsysmt.basic import get_form, convert, select

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="PDBFixer":

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.missingTerminals = {}

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, syntaxis=syntaxis, check=False)

        aux_dict = {}

        for group, atoms in temp_molecular_system.missingAtoms.items():
            if group.index in group_indices_in_selection:
                aux_dict[group]=[]
                for atom in atoms:
                    aux_dict[group].append(atom)

        temp_molecular_system.missingAtoms = aux_dict

        temp_molecular_system.addMissingAtoms()

    else:

        raise NotImplementedError

    output_molecular_system = convert(temp_molecular_system, to_form=form_out)

    return output_molecular_system

