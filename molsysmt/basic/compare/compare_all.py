from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def compare_all_eq(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    report = {}

    from molsysmt.basic import select, get

    molecular_system_A = digest_molecular_system(molecular_system_A)
    molecular_system_B = digest_molecular_system(molecular_system_B)

    # Number of atoms, groups, molecules, chains, entities

    n_atoms_A, n_groups_A, n_molecules_A, n_chains_A, n_entities_A, n_bonds_A = get(molecular_system_A,
            target='atom', selection=selection_A, n_atoms=True, n_groups=True, n_molecules=True,
            n_chains=True, n_entities=True, n_inner_bonds=True)

    n_atoms_B, n_groups_B, n_molecules_B, n_chains_B, n_entities_B, n_bonds_B = get(molecular_system_B,
            target='atom', selection=selection_B, n_atoms=True, n_groups=True, n_molecules=True,
            n_chains=True, n_entities=True, n_inner_bonds=True)


    report['n_atoms'] = (n_atoms_A == n_atoms_B)
    report['n_groups'] = (n_groups_A == n_groups_B)
    report['n_molecules'] = (n_molecules_A == n_molecules_B)
    report['n_chains'] = (n_chains_A == n_chains_B)
    report['n_entities'] = (n_entities_A == n_entities_B)
    report['n_bonds'] = (n_bonds_A == n_bonds_B)

    # Atoms

    if report['n_atoms']:

        atom_names_A, atom_types_A, atom_ids_A = get(molecular_system_A, target='atom',
                selection=selection_A, atom_name=True, atom_type=True, atom_id=True)

        atom_names_B, atom_types_B, atom_ids_B = get(molecular_system_B, target='atom',
                selection=selection_B, atom_name=True, atom_type=True, atom_id=True)

        report['atom_names'] = np.all(atom_names_A == atom_names_B)
        report['atom_types'] = np.all(atom_types_A == atom_types_B)
        report['atom_ids'] = np.all(atom_ids_A == atom_ids_B)

    else:

        report['atom_names'] = False
        report['atom_types'] = False
        report['atom_ids'] = False

    # Groups

    if report['n_groups']:

        group_names_A, group_types_A, group_ids_A = get(molecular_system_A, target='group',
                selection=selection_A, group_name=True, group_type=True, group_id=True)

        group_names_B, group_types_B, group_ids_B = get(molecular_system_B, target='group',
                selection=selection_B, group_name=True, group_type=True, group_id=True)

        report['group_names'] = np.all(group_names_A == group_names_B)
        report['group_types'] = np.all(group_types_A == group_types_B)
        report['group_ids'] = np.all(group_ids_A == group_ids_B)

    else:

        report['group_names'] = False
        report['group_types'] = False
        report['group_ids'] = False


    # Molecules

    if report['n_molecules']:

        molecule_names_A, molecule_types_A, molecule_ids_A = get(molecular_system_A, target='molecule',
                selection=selection_A, molecule_name=True, molecule_type=True, molecule_id=True)

        molecule_names_B, molecule_types_B, molecule_ids_B = get(molecular_system_B, target='molecule',
                selection=selection_B, molecule_name=True, molecule_type=True, molecule_id=True)

        report['molecule_names'] = np.all(molecule_names_A == molecule_names_B)
        report['molecule_types'] = np.all(molecule_types_A == molecule_types_B)
        report['molecule_ids'] = np.all(molecule_ids_A == molecule_ids_B)

    else:

        report['molecule_names'] = False
        report['molecule_types'] = False
        report['molecule_ids'] = False

    # chains

    if report['n_chains']:

        chain_names_A, chain_types_A, chain_ids_A = get(molecular_system_A, target='chain',
                selection=selection_A, chain_name=True, chain_type=True, chain_id=True)

        chain_names_B, chain_types_B, chain_ids_B = get(molecular_system_B, target='chain',
                selection=selection_B, chain_name=True, chain_type=True, chain_id=True)

        report['chain_names'] = np.all(chain_names_A == chain_names_B)
        report['chain_types'] = np.all(chain_types_A == chain_types_B)
        report['chain_ids'] = np.all(chain_ids_A == chain_ids_B)

    else:

        report['chain_names'] = False
        report['chain_types'] = False
        report['chain_ids'] = False

    # entities

    if report['n_entities']:

        entity_names_A, entity_types_A, entity_ids_A = get(molecular_system_A, target='entity',
                selection=selection_A, entity_name=True, entity_type=True, entity_id=True)

        entity_names_B, entity_types_B, entity_ids_B = get(molecular_system_B, target='entity',
                selection=selection_B, entity_name=True, entity_type=True, entity_id=True)

        report['entity_names'] = np.all(entity_names_A == entity_names_B)
        report['entity_types'] = np.all(entity_types_A == entity_types_B)
        report['entity_ids'] = np.all(entity_ids_A == entity_ids_B)

    else:

        report['entity_names'] = False
        report['entity_types'] = False
        report['entity_ids'] = False


    # bonds

    if report['n_bonds']:

        bonded_atoms_A, bond_order_A, bond_type_A = get(molecular_system_A, target='bond',
                selection=selection_A, atom_index=True, bond_order=True, bond_type=True)

        bonded_atoms_B, bond_order_B, bond_type_B = get(molecular_system_B, target='bond',
                selection=selection_A, atom_index=True, bond_order=True, bond_type=True)

        report['bonded_atoms'] = np.all(bonded_atoms_A == bonded_atoms_B)
        report['bond_order'] = np.all(bond_order_A == bond_order_B)
        report['bond_type'] = np.all(bond_type_A == bond_type_B)

    else:

        report['bonded_atoms'] = False
        report['bond_order'] = False
        report['bond_type'] = False


    # coordinates

    if report['n_atoms']:

        coordinates_A = get(molecular_system_A, target='atom',
                selection=selection_A, structure_indices=structure_indices_A, coordinates=True)

        coordinates_B = get(molecular_system_B, target='atom',
                selection=selection_B, structure_indices=structure_indices_B, coordinates=True)

        if coordinates_A is None:
            if coordinates_B is None:
                report['coordinates'] = True
            else:
                report['coordinates'] = False
        else:
            if coordinates_B is None:
                report['coordinates'] = False
            else:
                report['coordinates'] = np.allclose(coordinates_A, coordinates_B)

    else:

        report['coordinates'] = False

    # box

    box_A = get(molecular_system_A, target='system',
            selection=selection_A, structure_indices=structure_indices_A, box=True)

    box_B = get(molecular_system_B, target='system',
            selection=selection_B, structure_indices=structure_indices_B, box=True)

    if box_A is None:
        if box_B is None:
            report['box'] = True
        else:
            report['box'] = False
    else:
        if box_B is None:
            report['box'] = False
        else:
            report['box'] = np.allclose(box_A, box_B)

    # Report dictionary and result

    report = {key: value for key, value in report.items() if not value}
    result = (len(report)==0)

    return result, report


def compare_all_in(molecular_system_A, molecular_system_B, selection_A='all',
        structure_indices_A='all', selection_B='all', structure_indices_B='all', syntaxis='MolSysMT'):

    raise NotImplementedError()

