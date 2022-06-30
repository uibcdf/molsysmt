from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def add_missing_terminal_cappings(molecular_system, N_terminal=None, C_terminal=None, pH=7.4, selection='all',
                         syntaxis='MolSysMT', engine='PDBFixer', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        engine = digest_engine(engine)

    from molsysmt.basic import get_form, convert, get, select

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine is 'PDBFixer':

        from pdbfixer.pdbfixer import Sequence

        temp_molecular_system = convert(molecular_system, to_form='pdbfixer.PDBFixer')
        atom_indices_in_selection = select(temp_molecular_system, selection=selection, syntaxis=syntaxis, check=False)
        atom_indices_in_components = get(temp_molecular_system, element='component', selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection', atom_index=True)

        for atom_indices_in_component in atom_indices_in_components:

            chain_id = get(temp_molecular_system, element='chain', selection='atom_index in @atom_indices_in_component',
                           chain_id=True)
            groups_sequence = get(temp_molecular_system, element='group',
                                  selection='atom_index in @atom_indices_in_component', group_name=True)

            groups_sequence = list(groups_sequence)

            if N_terminal is not None:

                groups_sequence = [N_terminal]+groups_sequence

            if C_terminal is not None:

                groups_sequence = groups_sequence+[C_terminal]

            temp_molecular_system.sequences.append(Sequence(chain_id, groups_sequence))

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.addMissingAtoms()

        n_hs = get(temp_molecular_system, element='atom', selection='atom_type=="H"', n_atoms=True)

        if n_hs > 0:

            temp_molecular_system.addMissingHydrogens(pH)

        output_molecular_system = temp_molecular_system

    else:

        raise NotImplementedError

    output_molecular_system = convert(output_molecular_system, to_form=form_out)

    return output_molecular_system

