from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest()
def add_missing_heavy_atoms(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    To be written soon...
    """

    from molsysmt.basic import get_form, convert, select, get, set

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="PDBFixer":

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        atts_from_groups = get(molecular_system, element='group', component_id=True, component_name=True,
                               molecule_id=True, molecule_name=True, chain_name=True,
                               entity_index=True, entity_id=True, entity_name=True, entity_type=True,
                               output_type='dictionary')

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.missingTerminals = {}

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, syntax=syntax)

        aux_dict = {}

        for group, atoms in temp_molecular_system.missingAtoms.items():
            if group.index in group_indices_in_selection:
                aux_dict[group]=[]
                for atom in atoms:
                    aux_dict[group].append(atom)

        temp_molecular_system.missingAtoms = aux_dict

        temp_molecular_system.addMissingAtoms()

        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='group', **atts_from_groups)

        del(atts_from_groups, group_indices_in_selection, temp_molecular_system)

    else:

        raise NotImplementedMethodError


    return output_molecular_system

