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
    assert not rows["build.infer_covalent_bonds"]["exposed"]
    for name in (
        "get_donor_atoms",
        "get_acceptor_atoms",
        "get_hbond_sites",
        "get_hbond_site_directions",
    ):
        assert rows[f"interactions.hbonds.{name}"]["exposed"]
    assert not rows["interactions.hbonds.get_hbonds"]["exposed"]
    assert not rows["molecular_mechanics.get_forces"]["exposed"]
    assert (
        rows["basic.are_multiple_molecular_systems"]["input_kind"]
        == "explicit_collection"
    )
    assert rows["basic.add"]["input_kind"] == "primary"
    assert rows["attribute.get_argument_aliases"]["input_kind"] == "explicit_inputs"
    assert not rows["supported.forms"]["exposed"]
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
