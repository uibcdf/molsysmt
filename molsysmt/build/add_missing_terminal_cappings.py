from molsysmt._private.digestion import digest

@digest()
def add_missing_terminal_cappings(molecular_system, N_terminal=None, C_terminal=None, pH=7.4, 
                                  keep_ids=False, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    To be written soon...
    """

    from molsysmt.basic import get_form

    output_molecular_system = None
    form_in = get_form(molecular_system)

    if engine == 'PDBFixer':

        from molsysmt.basic import convert, get, select, has_attribute, set
        from pdbfixer.pdbfixer import Sequence

        temp_molecular_system = convert(molecular_system, to_form='pdbfixer.PDBFixer')
        atom_indices_in_selection = select(temp_molecular_system, selection=selection, syntax=syntax)
        atom_indices_in_components = get(temp_molecular_system, element='component', selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection', atom_index=True)

        temp_molecular_system.findMissingResidues()

        for atom_indices_in_component in atom_indices_in_components:

            chain_index = get(temp_molecular_system, element='chain', selection='atom_index in @atom_indices_in_component',
                           chain_index=True)[0]

            n_groups = get(temp_molecular_system, element='group',
                           selection='atom_index in @atom_indices_in_component', n_groups=True)

            if N_terminal is not None:

                temp_molecular_system.missingResidues[(chain_index,0)]=[N_terminal]

            if C_terminal is not None:

                temp_molecular_system.missingResidues[(chain_index,n_groups)]=[C_terminal]

        print(temp_molecular_system.missingResidues)

        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.addMissingAtoms()

        n_hs = get(temp_molecular_system, element='atom', selection='atom_type=="H"', n_atoms=True)

        if n_hs > 0:

            temp_molecular_system.addMissingHydrogens(pH)

        output_molecular_system = convert(temp_molecular_system, to_form=form_in)

        if has_attribute(molecular_system, 'component_name'):
            component_names = get(molecular_system, element='component', component_name=True)
            set(output_molecular_system, element='component', component_name=component_names)

        if has_attribute(molecular_system, 'molecule_name'):
            molecule_names = get(molecular_system, element='molecule', molecule_name=True)
            set(output_molecular_system, element='molecule', molecule_name=molecule_names)

        if has_attribute(molecular_system, 'entity_name'):
            entity_names = get(molecular_system, element='entity', entity_name=True)
            set(output_molecular_system, element='entity', entity_name=entity_names)

        if keep_ids:
            raise NotImplementedError

        return output_molecular_system

    else:

        raise NotImplementedError


