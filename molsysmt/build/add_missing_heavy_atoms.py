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

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary')
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary')
        #atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
        #                       chain_type=True, output_type='dictionary')
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
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

        return temp_molecular_system
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='component', **atts_from_components)
        set(output_molecular_system, element='molecule', **atts_from_molecules)
        #set(output_molecular_system, element='chain', **atts_from_chains)
        set(output_molecular_system, element='entity', **atts_from_entities)

        del(group_indices_in_selection, temp_molecular_system)
        #del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)
        del(atts_from_components, atts_from_molecules, atts_from_entities)

    else:

        raise NotImplementedMethodError


    return output_molecular_system

