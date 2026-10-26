"""Check output-only PDBQT presentation and maps bound to final actual bytes."""

import hashlib
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, FormatError
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol, unchanged


def tree(source):
    # Root packed in a different order; the child endpoint must lead its fragment.
    return {
        "schema_version": "molsysmt.pdbqt-torsion-tree@1",
        "atom_ids": source.topology.atoms.atom_id.to_numpy(copy=True),
        "fragment_atom_indices": np.array([4, 2, 3, 0, 5, 1], dtype=np.int64),
        "fragment_offsets": np.array([0, 4, 6], dtype=np.int64),
        "branch_atom_pairs": np.array([[0, 1]], dtype=np.int64),
        "branch_fragment_pairs": np.array([[0, 1]], dtype=np.int64),
        "root_fragment_index": 0,
        "torsdof": 1,
    }


def presentation():
    return {
        "atom_serials": "consecutive",
        "atom_names": ["C1", "O1", "H2", "H3", "H4", "H5"],
        "group_names": "LIG",
        "group_ids": "1",
        "chain_ids": "A",
        "occupancy": 1.0,
        "b_factor": puw.quantity(0.02, "nm**2"),
    }


def export(source, route, target, tmp_path, **kwargs):
    if route == "public":
        if target == "file:pdbqt":
            kwargs["output_filename"] = tmp_path / "out.pdbqt"
        return msm.convert(source, to_form=target, **kwargs)
    from molsysmt.form import _dict_modules, load_converter

    module = _dict_modules["molsysmt.MolSys"]
    converter = load_converter(module, module._convert_to[target])
    kwargs["atom_indices"] = kwargs.pop("selection", "all")
    if target == "file:pdbqt":
        kwargs["output_filename"] = tmp_path / "out.pdbqt"
    return converter(source, **kwargs)


def payload(output, target):
    return (
        Path(output).read_text()
        if target == "file:pdbqt"
        else output.removeprefix("pdbqt_text:")
    )


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("target", ["file:pdbqt", "string:pdbqt_text"])
@pytest.mark.parametrize("units", [["nm", "ps", "e"], ["pm", "fs", "coulomb"]])
def test_tree_presentation_preserves_source_and_binds_final_bytes(
    route, target, units, tmp_path
):
    source = declared_methanol()
    before = source.copy()
    original_tree = tree(source)
    options = presentation()
    remarks = [
        "REMARK DOCKINGMT_PARTIAL_CHARGES declared",
        "REMARK DOCKINGMT_ATOM_TYPES autodock4",
    ]
    with puw.context(standard_units=units):
        output, mapping = export(
            source,
            route,
            target,
            tmp_path,
            structure_indices=[2],
            typing_scheme="autodock4",
            torsion_tree=original_tree,
            output_presentation=options,
            remarks=remarks,
            return_atom_map=True,
        )
    text = payload(output, target)
    rows = [line for line in text.splitlines() if line.startswith("ATOM  ")]
    order = [4, 2, 3, 0, 1, 5]
    assert [int(line[6:11]) for line in rows] == [1, 2, 3, 4, 5, 6]
    assert [line[12:16].strip() for line in rows] == [
        options["atom_names"][i] for i in order
    ]
    assert all(
        line[17:20] == "LIG" and line[21] == "A" and int(line[22:26]) == 1
        for line in rows
    )
    np.testing.assert_allclose(
        [[float(line[start : start + 8]) for start in (30, 38, 46)] for line in rows],
        np.arange(54).reshape(3, 6, 3)[2, order],
    )
    np.testing.assert_allclose([float(line[54:60]) for line in rows], 1)
    np.testing.assert_allclose([float(line[60:66]) for line in rows], 2)
    np.testing.assert_allclose(
        [float(line[68:76]) for line in rows],
        np.array([-0.4, -0.5, 0.1, 0.2, 0.3, 0.3])[order],
    )
    assert "BRANCH 4 5\n" in text and "ENDBRANCH 4 5\n" in text
    assert text.startswith("\n".join(remarks) + "\nROOT\n")
    assert mapping["source_atom_ids"].tolist() == before.topology.atoms.atom_id.tolist()
    assert mapping["output_atom_ids"].tolist() == [str(i) for i in range(1, 7)]
    np.testing.assert_array_equal(mapping["output_to_source_atom_indices"], order)
    np.testing.assert_array_equal(mapping["branch_source_atom_pairs"], [[0, 1]])
    assert mapping["payload_sha256"] == hashlib.sha256(text.encode("utf-8")).hexdigest()
    if target == "file:pdbqt":
        assert Path(output).read_bytes() == text.encode("utf-8")
    unchanged(source, before)
    assert source.topology.n_groups == source.topology.n_chains == 0
    assert options["atom_serials"] == "consecutive" and options["group_names"] == "LIG"
    np.testing.assert_array_equal(
        original_tree["fragment_atom_indices"], [4, 2, 3, 0, 5, 1]
    )


@pytest.mark.parametrize("route", ["direct", "public"])
def test_presentation_vectors_follow_original_source_axis_before_selection(
    route, tmp_path
):
    source = declared_methanol()
    options = presentation()
    options.update(
        atom_serials=[51, 12, 33, 90, 45, 24],
        group_names=list("ABCDEF"),
        occupancy=np.arange(6) / 10,
        b_factor=puw.quantity(np.arange(6) / 100, "nm**2"),
    )
    output, mapping = export(
        source,
        route,
        "string:pdbqt_text",
        tmp_path,
        selection=[5, 1, 0],
        structure_indices=[1],
        typing_scheme="autodock4",
        output_presentation=options,
        return_atom_map=True,
    )
    rows = [
        line
        for line in payload(output, "string:pdbqt_text").splitlines()
        if line.startswith("ATOM  ")
    ]
    assert [int(line[6:11]) for line in rows] == [51, 12, 24]
    assert [line[17:20].strip() for line in rows] == ["A", "B", "F"]
    np.testing.assert_allclose([float(line[54:60]) for line in rows], [0, 0.1, 0.5])
    np.testing.assert_allclose([float(line[60:66]) for line in rows], [0, 1, 5])
    assert mapping["output_to_source_atom_indices"].tolist() == [0, 1, 5]
    assert mapping["source_to_output_atom_indices"].tolist() == [0, 1, -1, -1, -1, 2]


@pytest.mark.parametrize("ids", [["C0", "O1", "H2", "H3", "H4", "H5"], ["0"] * 6])
def test_explicit_serial_presentation_does_not_require_numeric_unique_source_ids(
    ids, tmp_path
):
    source = declared_methanol()
    source.topology.atoms["atom_id"] = ids
    before = source.copy()
    output, mapping = export(
        source,
        "public",
        "string:pdbqt_text",
        tmp_path,
        structure_indices=[0],
        typing_scheme="autodock4",
        output_presentation={"atom_serials": "consecutive"},
        return_atom_map=True,
    )
    assert mapping["source_atom_ids"].tolist() == ids
    assert mapping["output_atom_ids"].tolist() == [str(i) for i in range(1, 7)]
    unchanged(source, before)


@pytest.mark.parametrize(
    "options,remarks",
    [
        ({"partial_charge": 0}, None),
        ({"atom_serials": [1] * 6}, None),
        ({"atom_serials": [0, 1, 2, 3, 4, 5]}, None),
        ({"atom_serials": "automatic"}, None),
        ({"atom_names": "ABCDE"}, None),
        ({"group_names": "TOOLONG"}, None),
        ({"chain_ids": "AB"}, None),
        ({"atom_names": "C\nEND"}, None),
        ({"atom_names": "C\x00"}, None),
        ({"atom_names": puw.quantity([1] * 6, "nm")}, None),
        ({"occupancy": np.complex64(1j)}, None),
        ({"occupancy": np.nan}, None),
        ({"occupancy": 1 + 2j}, None),
        ({"b_factor": 0.0}, None),
        ({"b_factor": puw.quantity(1, "nm")}, None),
        ({"atom_names": ["A", "B"]}, None),
        ({}, ["ATOM      1"]),
        ({}, ["REMARK ok\nEND"]),
        ({}, ["REMARK MOLSYSMT_PARTIAL_CHARGES forged"]),
        ({}, ["REMARK \x00bad"]),
        ({}, ["REMARK " + "X" * 4096]),
        ({}, "REMARK text"),
        ({}, ["REMARK " + "X" * 4000] * 17),
        ({}, ["REMARK   molsysmt_forged data"]),
    ],
)
def test_bad_presentation_or_remarks_preserve_existing_destination(
    options, remarks, tmp_path
):
    source = declared_methanol()
    before = source.copy()
    filename = tmp_path / "out.pdbqt"
    filename.write_bytes(b"existing bytes\r\n")
    with pytest.raises((ArgumentError, FormatError)):
        export(
            source,
            "public",
            "file:pdbqt",
            tmp_path,
            structure_indices=[0],
            typing_scheme="autodock4",
            output_presentation=options,
            remarks=remarks,
        )
    assert filename.read_bytes() == b"existing bytes\r\n"
    unchanged(source, before)


@pytest.mark.parametrize("ligand", [False, True])
def test_defaults_stay_identical_and_optional_fields_can_be_cleared(ligand, tmp_path):
    source = declared_methanol()
    kwargs = dict(
        structure_indices=[0], typing_scheme="autodock4", return_atom_map=True
    )
    if ligand:
        kwargs["torsion_tree"] = tree(source)
    original, baseline = export(
        source, "public", "string:pdbqt_text", tmp_path, **kwargs
    )
    for options in ({}, {"atom_serials": "preserve"}):
        text, mapping = export(
            source,
            "public",
            "string:pdbqt_text",
            tmp_path,
            output_presentation=options,
            remarks=[],
            **kwargs,
        )
        assert text == original
        assert mapping["payload_sha256"] == baseline["payload_sha256"]
    source.structures.occupancy = np.ones((3, 6))
    source.structures.b_factor = puw.quantity(np.ones((3, 6)), "nm**2")
    text, _ = export(
        source,
        "public",
        "string:pdbqt_text",
        tmp_path,
        output_presentation={"occupancy": None, "b_factor": None},
        **kwargs,
    )
    assert all(
        line[54:66] == " " * 12
        for line in text.splitlines()
        if line.startswith("ATOM  ")
    )


@pytest.mark.parametrize("named", [False, True])
def test_presentation_composes_through_hydrogen_projection_and_known_poses(
    named, tmp_path
):
    import json

    from tests.form.file_pdbqt.test_known_source_poses import ensemble, rigid_tree

    if named:
        pytest.importorskip("rdkit.Chem")
        from tests.build.test_assign_autodock_atom_types import prepared

        source = msm.build.assign_autodock_atom_types(
            prepared("CO"), typing_scheme="autodock4"
        )
        source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    else:
        source = declared_methanol()
    before = source.copy()
    projected = msm.build.merge_nonpolar_hydrogens(
        source, typing_scheme="autodock4", return_report=True
    )
    reduced = projected["molecular_system"]
    text, exported = export(
        reduced,
        "public",
        "string:pdbqt_text",
        tmp_path,
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(reduced, [1, 0, 2]),
        output_presentation={
            "atom_serials": "consecutive",
            "atom_names": ["C1", "O1", "H1"],
            "group_names": "LIG",
            "group_ids": "1",
            "chain_ids": "A",
        },
        remarks=['REMARK DOCKINGMT_PARTIAL_CHARGES {"consumer":"test"}'],
        return_atom_map=True,
    )
    parsed = msm.form.string_pdbqt_text.read_poses(
        ensemble(text), reduced, exported, return_report=True
    )
    combined = msm.compose_atom_maps([projected["report"], exported, parsed["report"]])
    assert combined["output_to_source_atom_indices"].tolist() == [0, 1, 5]
    assert combined["source_to_representative_atom_indices"].tolist() == [
        0,
        1,
        0,
        0,
        0,
        2,
    ]
    assert (
        parsed["molecular_system"].topology.atoms.atom_id.tolist()
        == reduced.topology.atoms.atom_id.tolist()
    )
    expected = puw.get_value(reduced.structures.coordinates, to_unit="nm")[0]
    actual = puw.get_value(
        parsed["molecular_system"].structures.coordinates, to_unit="nm"
    )
    np.testing.assert_allclose(
        actual, expected[None] + np.array([0, 1, -0.5])[:, None, None], atol=0.00005
    )
    body = text.removeprefix("pdbqt_text:")
    assert exported["payload_sha256"] == hashlib.sha256(body.encode()).hexdigest()
    assert exported["output_atom_ids"].tolist() == ["1", "2", "3"]
    assert exported["output_to_source_atom_indices"].tolist() == [1, 0, 2]
    if named:
        for prefix, attribute in [
            ("MOLSYSMT_PARTIAL_CHARGES", "partial_charge_assignment"),
            ("MOLSYSMT_ATOM_TYPES", "atom_type_assignment"),
        ]:
            provider = json.loads(
                next(
                    line.removeprefix("REMARK " + prefix + " ")
                    for line in body.splitlines()
                    if line.startswith("REMARK " + prefix + " ")
                )
            )
            assert (
                provider["software"]
                == getattr(reduced.molecular_mechanics, attribute)["software"]
            )
            assert (
                provider["source_coverage"]
                == getattr(reduced.molecular_mechanics, attribute)["coverage"]
            )
            assert (
                provider["status"]
                == getattr(reduced.molecular_mechanics, attribute)["status"]
            )
    unchanged(source, before)


@pytest.mark.parametrize(
    "case", ["1iep", "1s63", "5x72-p59", "5x72-p69", "1iep-receptor"]
)
def test_real_prepared_corpus_presentation_preserves_chemical_fields(
    case, vina_reference_corpus, tmp_path
):
    root, records = vina_reference_corpus
    path = root / records[case]["files"]["pdbqt"]["filename"]
    source = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    before = source.copy()
    declared_tree = msm.form.file_pdbqt.get_torsion_tree(path)
    output, mapping = export(
        source,
        "public",
        "file:pdbqt",
        tmp_path,
        typing_scheme="autodock4",
        torsion_tree=declared_tree,
        output_presentation={
            "atom_serials": "consecutive",
            "group_names": "LIG",
            "group_ids": "1",
            "chain_ids": "A",
            "occupancy": 1,
            "b_factor": puw.quantity(0, "angstrom**2"),
        },
        remarks=['REMARK DOCKINGMT_ATOM_TYPES {"profile":"autodock4"}'],
        return_atom_map=True,
    )
    rows = [
        line
        for line in Path(output).read_text().splitlines()
        if line.startswith("ATOM  ")
    ]
    inverse = mapping["output_to_source_atom_indices"]
    assert [int(line[6:11]) for line in rows] == list(range(1, len(rows) + 1))
    np.testing.assert_array_equal(
        [line[77:].strip() for line in rows],
        np.asarray(source.molecular_mechanics.atom_ff_type)[inverse],
    )
    np.testing.assert_allclose(
        [float(line[68:76]) for line in rows],
        np.asarray(source.molecular_mechanics.partial_charge, dtype=float)[inverse],
        atol=0.0005,
    )
    np.testing.assert_allclose(
        [[float(line[start : start + 8]) for start in (30, 38, 46)] for line in rows],
        puw.get_value(source.structures.coordinates, to_unit="angstrom")[0, inverse],
        atol=0.0005,
    )
    assert (
        mapping["payload_sha256"]
        == hashlib.sha256(Path(output).read_bytes()).hexdigest()
    )
    unchanged(source, before)


@pytest.mark.parametrize(
    "case", ["1iep", "1s63", "5x72-p59", "5x72-p69", "1iep-receptor"]
)
def test_real_presented_output_is_accepted_by_vina(
    case, vina_reference_corpus, tmp_path
):
    vina = pytest.importorskip("vina")
    root, records = vina_reference_corpus
    path = root / records[case]["files"]["pdbqt"]["filename"]
    source = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    output = export(
        source,
        "public",
        "file:pdbqt",
        tmp_path,
        typing_scheme="autodock4",
        torsion_tree=msm.form.file_pdbqt.get_torsion_tree(path),
        output_presentation={
            "atom_serials": "consecutive",
            "group_names": "LIG",
            "group_ids": "1",
            "chain_ids": "A",
        },
        remarks=['REMARK DOCKINGMT_ATOM_TYPES {"profile":"autodock4"}'],
    )
    engine = vina.Vina(cpu=1, verbosity=0)
    if case == "1iep-receptor":
        engine.set_receptor(str(output))
    else:
        engine.set_ligand_from_string(Path(output).read_text())
