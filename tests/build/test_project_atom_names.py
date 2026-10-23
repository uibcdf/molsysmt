"""Checking explicit label projection without inferring chemistry or atom identity."""

import json

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    FormatError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Structures
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol, unchanged
from tests.form.file_pdbqt.test_known_source_poses import ensemble, rigid_tree


def project(source, **kwargs):
    return msm.build.project_atom_names(source, target_form="file:pdbqt", **kwargs)


def test_reserves_later_unselected_names_and_retains_full_axis():
    source = declared_methanol()
    msm.set(source, atom_name=["H1291", "H0", "H1292", "H1", "H2", "HD"])
    before = source.copy()
    result = project(source, selection=[2, 0, 2], return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert output.topology.atoms.atom_name.tolist() == [
        "H3",
        "H0",
        "H4",
        "H1",
        "H2",
        "HD",
    ]
    assert output.get_n_atoms() == 6
    assert output.structures.n_structures == 3
    assert report["source_atom_names"].tolist() == [
        "H1291",
        "H0",
        "H1292",
        "H1",
        "H2",
        "HD",
    ]
    assert report["source_atom_ids"].tolist() == ["17", "3", "45", "90", "7", "11"]
    np.testing.assert_array_equal(report["source_to_output_atom_indices"], np.arange(6))
    np.testing.assert_array_equal(report["selected_atom_indices"], [0, 2])
    np.testing.assert_array_equal(report["renamed_atom_indices"], [0, 2])
    unchanged(source, before)
    assert np.shares_memory(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
    )
    msm.set(output, selection=[0], atom_name=["NEW"])
    assert source.topology.atoms.atom_name[0] == "H1291"
    assert report["output_atom_names"][0] == "H3"


def test_group_local_collisions_and_existing_duplicate_valid_labels():
    source = MolSys(n_atoms=6, n_groups=2)
    source.topology.atoms["group_index"] = [0, 0, 0, 1, 1, 1]
    msm.set(source, atom_name=["H1291", "H0", "H0", "H1292", "H0", "C"])
    result = project(source)
    assert result.topology.atoms.atom_name.tolist() == [
        "H1",
        "H0",
        "H0",
        "H1",
        "H0",
        "C",
    ]


@pytest.mark.parametrize(
    "name,expected",
    [
        ("", "X0"),
        (None, "X0"),
        ("Δ", "X0"),
        (" h hh", "H0"),
        ("\x01", "X0"),
        ("abcdx", "A0"),
    ],
)
def test_invalid_names_use_an_explicit_lexical_prefix(name, expected):
    source = MolSys(n_atoms=1)
    source.topology.atoms.loc[0, "atom_name"] = name
    result = project(source, return_report=True)
    assert result["report"]["source_atom_names"][0] == name
    assert result["molecular_system"].topology.atoms.atom_name[0] == expected


@pytest.mark.parametrize("selection", [None, [-1], [6], [True], [1.2], [[0, 1]]])
def test_invalid_selection_does_not_rename_source(selection):
    source = declared_methanol()
    before = source.topology.atoms.copy()
    with pytest.raises(ArgumentError):
        project(source, selection=selection)
    pd.testing.assert_frame_equal(source.topology.atoms, before)


@pytest.mark.parametrize("target", [None, "file:pdb", ["file:pdbqt"], "not_a_form"])
def test_unsupported_target_rejects_before_changes(target):
    source = declared_methanol()
    with pytest.raises(ArgumentError):
        msm.build.project_atom_names(source, target_form=target)


def test_report_boolean_and_empty_selection():
    source = declared_methanol()
    msm.set(source, atom_name=["too_long"] * 6)
    with pytest.raises(ArgumentError):
        project(source, return_report="yes")
    result = project(source, selection=[], return_report=True)
    assert result["report"]["renamed_atom_indices"].dtype == np.int64
    assert result["report"]["renamed_atom_indices"].shape == (0,)
    assert (
        result["molecular_system"].topology.atoms.atom_name.tolist() == ["too_long"] * 6
    )


def test_unknown_groups_use_conservative_system_scope_and_missing_topology_rejects():
    source = MolSys(n_atoms=1)
    source.topology.atoms.loc[0, "group_index"] = pd.NA
    result = project(source, return_report=True)
    assert result["report"]["parameters"]["collision_scope"] == "system"
    source = MolSys._from_partial_domains(structures=Structures())
    with pytest.raises(StructuralInconsistencyError, match="topology"):
        project(source)


def test_empty_atom_axis_has_shaped_maps():
    result = project(MolSys(n_atoms=0), return_report=True)
    for name in [
        "source_to_output_atom_indices",
        "output_to_source_atom_indices",
        "renamed_atom_indices",
        "selected_atom_indices",
    ]:
        assert result["report"][name].shape == (0,)
        assert result["report"][name].dtype == np.int64
    composed = msm.basic.compose_atom_maps([result["report"]])
    assert composed["source_atom_status"].shape == (0,)


def test_namespace_exhaustion_never_applies_a_partial_rename():
    from molsysmt._private.atom_name_projection import project_labels

    names = np.array(
        ["H" + char for char in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + ["Hlong"],
        dtype=object,
    )
    original = names.copy()
    with pytest.raises(StructuralInconsistencyError, match="exhausted"):
        project_labels(names, [0] * len(names), [36], width=2)
    np.testing.assert_array_equal(names, original)


def test_counter_crosses_decimal_and_single_character_boundaries():
    source = MolSys(n_atoms=38)
    source.topology.atoms["atom_name"] = ["H-long"] * 38
    names = project(source).topology.atoms.atom_name.tolist()
    assert [names[i] for i in [0, 9, 10, 35, 36, 37]] == [
        "H0",
        "H9",
        "HA",
        "HZ",
        "H10",
        "H11",
    ]


def test_foreign_rdkit_labels_and_input_properties_are_preserved():
    Chem = pytest.importorskip("rdkit.Chem")
    source = Chem.MolFromSmiles("CO")
    for atom, name in zip(source.GetAtoms(), ["H1291", "H0"]):
        info = Chem.AtomPDBResidueInfo()
        info.SetName(name)
        info.SetResidueName("LIG")
        info.SetResidueNumber(1)
        atom.SetMonomerInfo(info)
    before = source.ToBinary(Chem.PropertyPickleOptions.AllProps)
    result = project(source, return_report=True)
    assert result["report"]["source_atom_names"].tolist() == ["H1291", "H0"]
    assert result["report"]["output_atom_names"].tolist() == ["H1", "H0"]
    assert source.ToBinary(Chem.PropertyPickleOptions.AllProps) == before


def test_user_guide_examples_execute():
    import re
    from pathlib import Path

    page = (
        Path(__file__).parents[2]
        / "docs/content/user/tools/build/project_atom_names.md"
    )
    scope = {}
    for code in re.findall(r"```python\n(.*?)```", page.read_text(), flags=re.S):
        exec(compile(code, str(page), "exec"), scope)
    assert scope["restored"]["source_atom_names"].tolist() == ["C-long", "H1291", "H0"]


@pytest.mark.parametrize("form", ["molsysmt.Topology", "molsysmt.MolSysDict"])
def test_form_agnostic_inputs(form):
    source = MolSys(n_atoms=6, n_groups=1)
    source.topology.atoms["group_index"] = [0] * 6
    msm.set(source, atom_name=["H1291", "H0", "H1292", "H1", "H2", "HD"])
    item = msm.convert(source, to_form=form)
    result = project(item)
    assert msm.get_form(result) == "molsysmt.MolSys"
    assert result.topology.atoms.atom_name.tolist() == [
        "H3",
        "H0",
        "H4",
        "H1",
        "H2",
        "HD",
    ]


def test_rename_merge_rooted_export_pose_and_json_composition():
    source = declared_methanol()
    msm.set(
        source, atom_name=["C_long", "O_long", "H_long", "H_long", "H_long", "H1291"]
    )
    renamed = project(source, return_report=True)
    reduced = msm.build.merge_nonpolar_hydrogens(
        renamed["molecular_system"], typing_scheme="autodock4", return_report=True
    )
    output = reduced["molecular_system"]
    text, exported = msm.convert(
        output,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(output, [2, 0, 1]),
        return_atom_map=True,
    )
    read = msm.form.string_pdbqt_text.read_poses(
        ensemble(text), output, exported, return_report=True
    )
    maps = [renamed["report"], reduced["report"], exported, read["report"]]
    result = msm.basic.compose_atom_maps(maps)
    assert result["source_atom_names"].tolist() == [
        "C_long",
        "O_long",
        "H_long",
        "H_long",
        "H_long",
        "H1291",
    ]
    assert result["output_atom_names"].tolist() == ["C0", "O0", "H3"]
    assert result["output_to_source_atom_indices"].tolist() == [0, 1, 5]
    assert result["stages"][0]["renamed_atom_indices"].tolist() == list(range(6))
    restored = msm.basic.compose_atom_maps(
        json.loads(json.dumps(maps, default=lambda value: value.tolist()))
    )
    np.testing.assert_array_equal(
        restored["source_to_output_atom_indices"], [0, 1, -1, -1, -1, 2]
    )
    assert (
        restored["source_atom_ids"].tolist() == source.topology.atoms.atom_id.tolist()
    )


def test_writer_still_rejects_unprojected_invalid_names():
    source = declared_methanol()
    msm.set(source, atom_name=["H1291", "O", "H2", "H3", "H4", "HD"])
    with pytest.raises(FormatError, match="name"):
        msm.convert(
            source,
            to_form="string:pdbqt_text",
            structure_indices=[0],
            typing_scheme="autodock4",
        )

    result = project(source, selection=[1])
    with pytest.raises(FormatError, match="name"):
        msm.convert(
            result,
            to_form="string:pdbqt_text",
            structure_indices=[0],
            typing_scheme="autodock4",
        )


def test_real_generation_named_assignments_rename_and_export_preserve_provenance():
    pytest.importorskip("rdkit.Chem")
    from tests.build.add_missing_hydrogens.test_fixed_state import hydrogenate, prepared

    source = prepared("CO", [[0, 0, 0], [1.4, 0, 0]])
    source.topology.atoms["atom_id"] = ["17", "3"]
    added = hydrogenate(source)
    typed = msm.build.assign_autodock_atom_types(
        added["molecular_system"], typing_scheme="autodock4"
    )
    typed = msm.build.assign_partial_charges(typed, method="gasteiger_marsili")
    msm.set(
        typed,
        atom_name=["carbon-long", "oxygen-long"] + [f"H{1291 + i}" for i in range(4)],
    )
    before = typed.copy()
    with msm.pyunitwizard.context(standard_units=["pm", "coulomb"]):
        renamed = project(typed, return_report=True)
    unchanged(typed, before)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(
            renamed["molecular_system"].structures.coordinates, to_unit="angstrom"
        ),
        msm.pyunitwizard.get_value(typed.structures.coordinates, to_unit="angstrom"),
    )

    def normalize(report):
        return json.dumps(report, sort_keys=True, default=lambda a: a.tolist())

    for name in ("atom_type_assignment", "partial_charge_assignment"):
        assert normalize(getattr(typed.molecular_mechanics, name)) == normalize(
            getattr(renamed["molecular_system"].molecular_mechanics, name)
        )
    reduced = msm.build.merge_nonpolar_hydrogens(
        renamed["molecular_system"], typing_scheme="autodock4", return_report=True
    )
    output = reduced["molecular_system"]
    text, exported = msm.convert(
        output,
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(output, [2, 0, 1]),
        return_atom_map=True,
    )
    read = msm.form.string_pdbqt_text.read_poses(
        ensemble(text), output, exported, return_report=True
    )
    mapped = msm.basic.compose_atom_maps(
        [
            added["report"],
            renamed["report"],
            reduced["report"],
            exported,
            read["report"],
        ]
    )
    assert mapped["output_to_source_atom_indices"].tolist() == [0, 1, -1]
    assert mapped["stages"][1]["operation"] == "atom_name_projection"
    assert mapped["stages"][0]["attribution"] == added["report"]["attribution"]
    assert exported["total_charge_before_rounding"] == pytest.approx(0, abs=1e-12)


def test_template_sensitive_charge_binding_is_not_recertified_after_rename():
    from molsysmt._private.partial_charges import bind_assignment, validate_assignment

    source = declared_methanol()
    msm.set(source, atom_name=["C-long", "O", "H1", "H2", "H3", "HD"])
    # A declared fixture binding tests the stale-name mechanism; this is not a
    # claimed execution of a force-field charge calculation.
    source.molecular_mechanics.partial_charge_assignment = bind_assignment(
        source, {"method": "forcefield", "chemical_state_index": 0}
    )
    validate_assignment(source)
    output = project(source)
    validate_assignment(source)
    with pytest.raises(StructuralInconsistencyError, match="bound chemistry"):
        validate_assignment(output)


def test_large_label_axis_has_compact_maps_and_deterministic_base36():
    source = MolSys(n_atoms=100_000, n_groups=10_000)
    source.topology.atoms["group_index"] = np.repeat(np.arange(10_000), 10)
    source.topology.atoms["atom_name"] = ["H-long"] * 100_000
    report = project(source, return_report=True)["report"]
    assert report["output_atom_names"][:10].tolist() == [f"H{i}" for i in range(10)]
    assert report["output_atom_names"][-1] == "H9"
    assert report["source_to_output_atom_indices"].nbytes == 800_000
    np.testing.assert_array_equal(report["renamed_atom_indices"], np.arange(100_000))


@pytest.mark.parametrize(
    "changes",
    [
        {"renamed_atom_indices": [-1]},
        {"renamed_atom_indices": [0, 0]},
        {"renamed_atom_indices": [[0]]},
        {"selected_atom_indices": [], "renamed_atom_indices": [0]},
    ],
)
def test_composition_rejects_invalid_declared_name_scope(changes):
    report = project(declared_methanol(), return_report=True)["report"]
    report.update(changes)
    with pytest.raises(StructuralInconsistencyError):
        msm.basic.compose_atom_maps([report])
