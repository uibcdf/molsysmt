from molsysmt._private.digestion import digest

@digest()
def add_missing_hydrogens(molecular_system, pH=7.4, forcefield='AMBER99SB-ILDN', engine='OpenMM'):

    from molsysmt.basic import convert, get_form

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="OpenMM":

        temp_molecular_system = convert(molecular_system, to_form="openmm.Modeller")
        log_residues_changed = temp_molecular_system.addHydrogens(pH=pH)

    elif engine=='PDBFixer':

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        temp_molecular_system.addMissingHydrogens(pH=pH)

    else:

        raise NotImplementedError

    output_molecular_system = convert(temp_molecular_system, to_form=form_out)

    return output_molecular_system

