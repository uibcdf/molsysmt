import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _assert_native_core_equal(observed, expected):
    for table_name in ("atoms", "groups", "components", "molecules", "chains", "entities", "bonds"):
        observed_table = getattr(observed.topology, table_name)
        expected_table = getattr(expected.topology, table_name)
        assert observed_table.columns.tolist() == expected_table.columns.tolist()
        assert observed_table.astype("string").fillna("<missing>").to_dict("records") == (
            expected_table.astype("string").fillna("<missing>").to_dict("records")
        )

    np.testing.assert_allclose(
        puw.get_value(observed.structures.coordinates, to_unit="nm"),
        puw.get_value(expected.structures.coordinates, to_unit="nm"),
        rtol=0.0,
        atol=0.0,
    )
    np.testing.assert_allclose(
        puw.get_value(observed.structures.box, to_unit="nm"),
        puw.get_value(expected.structures.box, to_unit="nm"),
        rtol=0.0,
        atol=0.0,
    )
    np.testing.assert_allclose(
        puw.get_value(observed.structures.time, to_unit="ps"),
        puw.get_value(expected.structures.time, to_unit="ps"),
        rtol=0.0,
        atol=0.0,
    )
    assert observed.structures.structure_id.tolist() == expected.structures.structure_id.tolist()


def test_molsysdict_roundtrip_preserves_its_declared_schema(rich_molsys):
    declared = msm.convert(rich_molsys, to_form="molsysmt.MolSysDict")
    rebuilt = msm.convert(declared, to_form="molsysmt.MolSys")
    redeclared = msm.convert(rebuilt, to_form="molsysmt.MolSysDict")

    assert redeclared.data == declared.data


def test_molsys_yaml_applies_selection_and_roundtrips_declared_schema(rich_molsys, tmp_path):
    __import__("pytest").importorskip("yaml")
    filename = tmp_path / "selected.yaml"
    msm.convert(
        rich_molsys,
        to_form="file:molsys_yaml",
        selection=[2, 0],
        structure_indices=[2, 0],
        output_filename=str(filename),
    )
    output = msm.convert(str(filename), to_form="molsysmt.MolSysDict")

    assert [atom["atom_id"] for atom in output.data["topology"]["atoms"]] == ["100", "102"]
    assert output.data["structures"]["structure_id"] == [50, 10]
    assert np.asarray(output.data["structures"]["coordinates"]).shape == (2, 2, 3)
