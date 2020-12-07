
def add_terminal_capping(item, N_terminal=None, C_terminal=None, selection='all',
                            syntaxis='MolSysMT', engine='PDBFixer'):

    from molsysmt.multitool import get_form
    from molsysmt import convert

    form_in = get_form(item)

    if engine is 'PDBFixer':

        from pdbfixer.pdbfixer import Sequence
        from molsysmt import get

        tmp_item = convert(item, to_form='pdbfixer.PDBFixer')

        atom_indices_in_selection = get(tmp_item, target='atom', selection=selection,
                                        syntaxis=syntaxis, atom_index=True)

        atom_indices_in_components = get(tmp_item, target='component', selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection', atom_index=True)

        for atom_indices_in_component in atom_indices_in_components:

            chain_id = get(tmp_item, target='chain', selection='atom_index in @atom_indices_in_component', chain_id=True)
            groups_sequence = get(tmp_item, target='group', selection='atom_index in @atom_indices_in_component', group_name=True)

            groups_sequence = list(groups_sequence)

            if N_terminal is not None:

                groups_sequence = [N_terminal]+groups_sequence

            if C_terminal is not None:

                groups_sequence = groups_sequence+[C_terminal]

            tmp_item.sequences.append(Sequence(chain_id, groups_sequence))

        tmp_item.findMissingResidues()
        tmp_item.findMissingAtoms()
        tmp_item.addMissingAtoms()

        n_hs = get(tmp_item, target='atom', selection='atom_type=="H"', n_atoms=True)

        if n_hs > 0:

            tmp_item.addMissingHydrogens(pH=7.4)

        tmp_item = convert(tmp_item, to_form=form_in)

    else:

        raise NotImplementedError

    return tmp_item

