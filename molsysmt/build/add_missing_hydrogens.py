from molsysmt._private.digestion import digest

@digest()
def add_missing_hydrogens(molecular_system, pH=7.4, engine='OpenMM'):
#def add_missing_hydrogens(molecular_system, pH=7.4, forcefield='AMBER99SB-ILDN', engine='OpenMM'):

    from molsysmt.basic import convert, get_form, get, set

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="OpenMM":

        atts_from_groups = get(molecular_system, element='group', component_id=True, component_name=True,
                               molecule_id=True, molecule_name=True, chain_name=True,
                               entity_index=True, entity_id=True, entity_name=True, entity_type=True,
                               output_type='dictionary')

        temp_molecular_system = convert(molecular_system, to_form="openmm.Modeller")
        log_residues_changed = temp_molecular_system.addHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='group', **atts_from_groups)

        del(atts_from_groups, temp_molecular_system)

    elif engine=='PDBFixer':


        atts_from_groups = get(molecular_system, element='group', component_id=True, component_name=True,
                               molecule_id=True, molecule_name=True, chain_name=True,
                               entity_index=True, entity_id=True, entity_name=True, entity_type=True,
                               output_type='dictionary')

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        temp_molecular_system.addMissingHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='group', **atts_from_groups)

        del(atts_from_groups, temp_molecular_system)

    else:

        raise NotImplementedError


    return output_molecular_system

