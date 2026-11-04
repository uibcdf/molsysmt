"""Check real public declarations, unreceived routes and compatibility aliases."""

from devtools.scripts.audit_molsysviewer_tools_api import collect_inventory


def test_inventory_records_real_complete_and_missing_public_routes():
    inventory = collect_inventory()
    rows = {row["path"]: row for row in inventory["functions"]}
    assert rows["physchem.get_peptide_chemical_template"]["exposed"]
    assert (
        rows["physchem.get_peptide_chemical_template"]["input_kind"]
        == "explicit_inputs"
    )
    assert rows["build.get_peptide_bond_candidates"]["exposed"]
    for name in (
        "get_missing_heavy_atoms",
        "get_missing_bonds",
        "get_missing_residues",
        "get_missing_terminal_cappings",
        "get_non_standard_residues",
        "get_disulfide_bonds",
        "has_hydrogens",
        "is_solvated",
    ):
        assert rows[f"build.{name}"]["exposed"]
    for name in (
        "infer_covalent_bonds",
        "assign_autodock_atom_types",
        "assign_partial_charges",
        "project_atom_names",
    ):
        assert rows[f"build.{name}"]["exposed"]
        assert rows[f"build.{name}"]["input_kind"] == "primary"
    for path in [
        "basic.compose_atom_maps",
        "basic.add",
        "basic.append_structures",
        "basic.concatenate_structures",
        "basic.merge",
        "basic.permute_atoms",
        "h5msm.read",
        "h5msm.write",
        "h5msm.read_layers",
        "h5msm.write_layers",
        "h5msm.append_structures",
        "h5msm.migrate_04_to_05",
        "h5msm.migrate_to_05",
    ]:
        assert rows[path]["exposed"]
    assert inventory["modules"]["h5msm"]["missing"] == []
    for name in (
        "get_donor_atoms",
        "get_acceptor_atoms",
        "get_hbond_sites",
        "get_hbond_site_directions",
    ):
        assert rows[f"interactions.hbonds.{name}"]["exposed"]
    for path in [
        "interactions.hbonds.get_buch_hbonds",
        "interactions.hbonds.get_luzard_chandler_hbonds",
        "interactions.hbonds.get_hbonds",
        "interactions.disulfides.get_disulfide_candidates",
    ]:
        assert rows[path]["exposed"]
    for path in [
        "interactions.ionic.get_ionic_interactions",
        "interactions.hydrophobic.get_hydrophobic_interactions",
        "interactions.halogen_bonds.get_halogen_bonds",
    ]:
        assert rows[path]["exposed"]
    for path in [
        "interactions.metal_coordination.get_metal_coordination",
        "interactions.pi_pi.get_pi_pi_interactions",
        "interactions.cation_pi.get_cation_pi_interactions",
        "interactions.water_bridges.get_water_bridges",
    ]:
        assert rows[path]["exposed"]
    assert inventory["modules"]["interactions"]["missing"] == []
    assert not rows["molecular_mechanics.get_forces"]["exposed"]
    assert (
        rows["basic.are_multiple_molecular_systems"]["input_kind"]
        == "explicit_collection"
    )
    assert rows["basic.add"]["input_kind"] == "primary"
    assert rows["attribute.get_argument_aliases"]["input_kind"] == "explicit_inputs"
    received_elements = {
        "element.is_element",
        "element.is_composed_of",
        "element.atom.is_atom_type",
        "element.atom.normalize_atom_types",
        "element.atom.get_atom_type_from_atom_name",
        "element.atom.get_atom_type_from_atom_ff_type",
        "element.group.is_group_type",
        "element.group.get_group_type_from_group_name",
    }
    hierarchy_elements = {
        "element.chain.get_chain_id",
        "element.chain.get_chain_index",
        "element.chain.get_chain_name",
        "element.chain.get_chain_type",
        "element.entity.get_entity_id",
        "element.entity.get_entity_index",
        "element.entity.get_entity_name",
        "element.entity.get_entity_type",
        "element.entity.get_n_entities",
    }
    domain_elements = {
        "element.component.get_component_id",
        "element.component.get_component_index",
        "element.component.get_component_name",
        "element.component.get_component_type",
        "element.component.get_n_components",
        "element.molecule.get_molecule_id",
        "element.molecule.get_molecule_index",
        "element.molecule.get_molecule_name",
        "element.molecule.get_molecule_type",
        "element.molecule.get_n_molecules",
        "element.group.get_group_type",
        "element.group.small_molecule.small_molecule_is_amino_acid",
    }
    label_elements = {
        "element.group.terminal_capping.is_c_terminal_capping",
        "element.group.amino_acid.get_1_letter_code_from_name",
        "element.group.terminal_capping.is_n_terminal_capping",
        "element.group.amino_acid.get_standard_name",
        "element.group.small_molecule.is_small_molecule",
        "element.group.saccharide.is_saccharide",
        "element.molecule.is_molecule_type",
        "element.group.amino_acid.is_amino_acid",
        "element.group.ion.is_ion",
        "element.group.terminal_capping.is_terminal_capping",
        "element.group.nucleotide.is_nucleotide",
        "element.group.lipid.is_lipid",
        "element.group.water.is_water",
        "element.component.is_component_type",
    }
    template_elements = {
        "element.group.get_bonded_atom_pairs",
        "element.group.amino_acid.get_bonded_atom_pairs",
        "element.group.amino_acid.get_expected_heavy_atoms",
        "element.group.amino_acid.get_expected_hydrogens",
        "element.group.amino_acid.get_group_db",
        "element.group.ion.get_bonded_atom_pairs",
        "element.group.ion.get_group_db",
        "element.group.saccharide.get_bonded_atom_pairs",
        "element.group.saccharide.get_group_db",
        "element.group.small_molecule.get_bonded_atom_pairs",
        "element.group.small_molecule.get_group_db",
        "element.group.terminal_capping.get_bonded_atom_pairs",
        "element.group.terminal_capping.get_group_db",
        "element.group.water.get_bonded_atom_pairs",
    }
    actual_elements = {
        path
        for path, row in rows.items()
        if path.startswith("element.") and row["exposed"]
    }
    assert (
        actual_elements
        == received_elements
        | hierarchy_elements
        | domain_elements
        | label_elements
        | template_elements
    )
    assert all(
        rows[path]["input_kind"] == "primary"
        for path in hierarchy_elements | domain_elements
    )
    assert all(
        rows[path]["input_kind"] == "explicit_inputs"
        for path in received_elements | label_elements | template_elements
    )
    assert inventory["modules"]["element"]["missing"] == []
    assert rows["element.group.get_group_type"]["exposed"]
    for name in ("forms", "conversions", "dependencies", "syntaxes"):
        assert rows[f"supported.{name}"]["exposed"]
        assert rows[f"supported.{name}"]["input_kind"] == "explicit_inputs"
    assert inventory["modules"]["supported"]["missing"] == []
    assert inventory["modules"]["attribute"]["exposed_paths"] == 7
    assert inventory["modules"]["attribute"]["missing"] == []
    assert "supported.syntaxes" in rows
    assert rows["supported.syntaxes"]["declaration_status"] in {
        "callable_compatibility_module",
        "callable_unqualified",
    }
    for path in [
        "molecular_dynamics.run_NPT_equilibration",
        "molecular_dynamics.run_NVT_equilibration",
    ]:
        assert rows[path]["declaration_status"] == "not_implemented_stub"
        assert not rows[path]["exposed"]
    assert "h5msm.arg_digest" not in rows
    assert (
        rows["hbonds.get_buch_hbonds"]["implementation"]
        == rows["interactions.hbonds.get_buch_hbonds"]["implementation"]
    )
    for scope, counts in inventory["modules"].items():
        actual = [row for row in rows.values() if row["path"].split(".")[0] == scope]
        assert counts["native_paths"] == len(actual)
        assert counts["missing"] == [
            row["path"] for row in actual if not row["exposed"]
        ]
        assert counts["exposed_paths"] == sum(row["exposed"] for row in actual)
        assert all(row["signature"].startswith("(") for row in actual)
