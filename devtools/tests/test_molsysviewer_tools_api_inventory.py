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
    assert not rows["build.infer_covalent_bonds"]["exposed"]
    assert not rows["molecular_mechanics.get_forces"]["exposed"]
    assert (
        rows["basic.are_multiple_molecular_systems"]["input_kind"]
        == "explicit_collection"
    )
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
