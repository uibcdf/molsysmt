#!/usr/bin/env bash
set -euo pipefail

TIER="${1:-smoke}"

run_smoke() {
  pytest -q \
    tests/element/component/test_get_component_index.py \
    tests/topology/get_covalent_blocks/test_get_covalent_blocks_from_molsysmt_MolSys.py \
    tests/pbc/get_lengths_and_angles_from_box/test_get_lengths_and_angles_from_box.py \
    tests/structure/get_rmsd/test_get_rmsd_from_molsysmt_MolSys.py \
    tests/structure/test_distance_family_contract.py \
    tests/form/string_amino_acids_3/test_biopython_codec.py \
    tests/structure/principal_component_analysis/test_weighted_contract.py \
    tests/structure/center/test_center_contract.py \
    tests/documentation/test_center_examples.py \
    tests/structure/move_away/test_move_away_contract.py \
    tests/structure/flip/test_reflection_contract.py \
    tests/structure/get_center/test_get_center_extended.py::test_empty_atom_population_raises_argument_error_before_group_dispatch \
    tests/documentation/test_move_away_examples.py \
    tests/structure/align/test_sequence_alignment_contract.py \
    tests/documentation/test_sequence_alignment_examples.py \
    tests/basic/test_file_copy.py \
    tests/basic/test_file_copy_lifecycle.py \
    tests/form/test_raw_file_copy.py \
    tests/physchem/test_property_selection_contract.py \
    tests/physchem/get_hydrogen_inventory/test_inventory.py \
    tests/physchem/test_get_chemical_readiness.py \
    tests/physchem/test_get_aromatic_rings.py \
    tests/physchem/test_get_aromaticity.py \
    tests/physchem/test_get_charge_centers.py \
    tests/physchem/test_get_hydrophobic_sites.py \
    tests/physchem/test_get_halogen_bond_sites.py \
    tests/physchem/test_get_bulkiness.py \
    tests/physchem/test_get_tpsa.py \
    tests/physchem/test_get_lipophilicity.py \
    tests/physchem/test_descriptor_contributions.py \
    tests/physchem/test_get_autodock_atom_types.py \
    tests/physchem/test_get_cip_stereochemistry.py \
    tests/physchem/test_get_partial_charges.py \
    tests/form/molsysmt_Topology/test_atom_membership_order.py \
    tests/form/molsysmt_Topology/test_mdtraj_missing_hierarchy.py \
    tests/native/test_builder_inherited_molecules.py \
    tests/native/test_builder_atom_extension.py \
    tests/physchem/test_get_secondary_structure_propensity.py \
    tests/physchem/test_reference_metadata_ownership.py \
    tests/native/test_group_free_molecules.py \
    tests/topology/get_substructure_matches/test_reference_selections.py \
    tests/structure/test_dihedral_edit_contract.py
}

run_build_topology() {
  pytest -q \
    tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py \
    tests/topology/get_bondgraph/test_get_bondgraph_from_molsysmt_MolSys.py \
    tests/topology/get_covalent_chains/test_get_covalent_chains_from_molsysmt_MolSys.py
}

run_peptide_extended() {
  pytest -q -m peptide_parity tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py
}

case "${TIER}" in
  smoke)
    run_smoke
    ;;
  build_topology)
    run_build_topology
    ;;
  peptide_extended)
    run_peptide_extended
    ;;
  *)
    echo "Unknown tier: ${TIER}"
    echo "Usage: $0 [smoke|build_topology|peptide_extended]"
    exit 2
    ;;
esac
