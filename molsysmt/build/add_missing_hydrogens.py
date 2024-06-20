from molsysmt._private.digestion import digest

@digest()
def add_missing_hydrogens(molecular_system, pH=7.4, engine='OpenMM'):

    from molsysmt.basic import convert, get_form, get, set

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="OpenMM":

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary')
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary')
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary')
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary')

        temp_molecular_system = convert(molecular_system, to_form="openmm.Modeller")
        log_residues_changed = temp_molecular_system.addHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='component', **atts_from_components)
        set(output_molecular_system, element='molecule', **atts_from_molecules)
        set(output_molecular_system, element='chain', **atts_from_chains)
        if form_out=='molsysmt.MolSys':
            output_molecular_system.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                              redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)
        elif form_out=='molsysmt.Topology':
            output_molecular_system.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                     redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)


        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

        del(temp_molecular_system)

    elif engine=='PDBFixer':

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary')
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary')
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary')
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary')

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        temp_molecular_system.addMissingHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='component', **atts_from_components)
        set(output_molecular_system, element='molecule', **atts_from_molecules)
        set(output_molecular_system, element='chain', **atts_from_chains)
        if form_out=='molsysmt.MolSys':
            output_molecular_system.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                              redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)
        elif form_out=='molsysmt.Topology':
            output_molecular_system.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                     redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)


        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

        del(temp_molecular_system)

    else:

        raise NotImplementedError


    return output_molecular_system

