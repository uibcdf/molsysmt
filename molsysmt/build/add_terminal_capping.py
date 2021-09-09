def add_terminal_capping(molecular_system, N_terminal=None, C_terminal=None, selection='all',
                         syntaxis='MolSysMT', engine='PDBFixer'):

    from molsysmt.basic import get_form, convert
    from molsysmt import convert

    form_in = get_form(molecular_system)

    if engine is 'PDBFixer':

        from pdbfixer.pdbfixer import Sequence
        from molsysmt import get, select

        tmp_molecular_system = convert(molecular_system, to_form='pdbfixer.PDBFixer')
        atom_indices_in_selection = select(tmp_molecular_system, selection=selection, syntaxis=syntaxis)
        atom_indices_in_components = get(tmp_molecular_system, target='component', selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection', atom_index=True)

        for atom_indices_in_component in atom_indices_in_components:

            chain_id = get(tmp_molecular_system, target='chain', selection='atom_index in @atom_indices_in_component', chain_id=True)
            groups_sequence = get(tmp_molecular_system, target='group', selection='atom_index in @atom_indices_in_component', group_name=True)

            groups_sequence = list(groups_sequence)

            if N_terminal is not None:

                groups_sequence = [N_terminal]+groups_sequence

            if C_terminal is not None:

                groups_sequence = groups_sequence+[C_terminal]

            tmp_molecular_system.sequences.append(Sequence(chain_id, groups_sequence))

        tmp_molecular_system.findMissingResidues()
        tmp_molecular_system.findMissingAtoms()
        tmp_molecular_system.addMissingAtoms()

        n_hs = get(tmp_molecular_system, target='atom', selection='atom_type=="H"', n_atoms=True)

        if n_hs > 0:

            tmp_molecular_system.addMissingHydrogens(pH=7.4)

        tmp_molecular_system = convert(tmp_molecular_system, to_form=form_in)

    else:

        raise NotImplementedError

    return tmp_molecular_system

