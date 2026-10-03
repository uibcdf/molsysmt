"""Checking independent fixed-column PDBQT data, trees, units and explicit losses."""

import copy
import importlib.util

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    FormatError,
    NotCompatibleConversionError,
)
from molsysmt.form.file_pdbqt import get_torsion_tree

# These literal records intentionally use nonconsecutive serial IDs. Atom
# indices must follow line order, not the value or sorted order of those IDs.
ATOMS = [
    "ATOM     17   C1 LIG B   7       1.000   2.000   3.000  1.00 20.00     0.125 C",
    "ATOM      3   C2 LIG B   7       2.000   3.000   4.000  1.00 20.00    -0.100 A",
    "ATOM     45   O1 LIG B   7       3.000   4.000   5.000  1.00 20.00    -0.250 OA",
    "ATOM     90   H1 LIG B   7       4.000   5.000   6.000  1.00 20.00     0.225 HD",
]
RIGID = "\n".join([*ATOMS, "END", ""])
LIGAND = "\n".join(
    [
        "REMARK independent fixture",
        "ROOT",
        *ATOMS[:2],
        "ENDROOT",
        "BRANCH 17 45",
        *ATOMS[2:],
        "ENDBRANCH 17 45",
        "TORSDOF 2",
        "",
    ]
)


@pytest.fixture(params=["rigid", "ligand"])
def source(request, tmp_path):
    path = tmp_path / "system.pdbqt"
    path.write_text(RIGID if request.param == "rigid" else LIGAND)
    return path


def native(source):
    return msm.convert(source, to_form="molsysmt.MolSys", discard_torsion_tree=True)


def test_public_forms_getters_and_native_units(source):
    assert msm.get_form(source) == "file:pdbqt"
    text = msm.convert(source, to_form="string:pdbqt_text")
    assert msm.get_form(text) == "string:pdbqt_text"
    molsys = native(text)
    assert molsys.topology.atoms.atom_id.tolist() == ["17", "3", "45", "90"]
    assert molsys.topology.atoms.atom_type.tolist() == ["C", "C", "O", "H"]
    assert molsys.topology.groups.group_id.tolist() == ["7"]
    assert molsys.topology.chains.chain_id.tolist() == ["B"]
    assert molsys.chemical_states._states[0].connectivity_completeness == "partial"
    assert not msm.has_attribute(source, "formal_charge")
    assert not msm.has_attribute(source, "atom_is_aromatic")
    assert not msm.has_attribute(source, "bond_order")
    types, coords = msm.get(text, element="atom", atom_type=True, coordinates=True)
    assert types == ["C", "C", "O", "H"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(coords, to_unit="nm")[0],
        np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]) / 10,
    )
    assert msm.get(text, element="system", n_atoms=True) == 4
    assert msm.get(text, element="system", n_structures=True) == 1
    np.testing.assert_allclose(
        msm.get(text, element="atom", partial_charge=True), [0.125, -0.1, -0.25, 0.225]
    )
    np.testing.assert_array_equal(
        msm.get(text, element="atom", atom_ff_type=True), ["C", "A", "OA", "HD"]
    )
    combined = msm.get(
        text,
        element="atom",
        atom_type=True,
        atom_ff_type=True,
        partial_charge=True,
        coordinates=True,
        output_type="dictionary",
    )
    np.testing.assert_array_equal(combined["atom_ff_type"], ["C", "A", "OA", "HD"])
    np.testing.assert_allclose(combined["partial_charge"], [0.125, -0.1, -0.25, 0.225])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(molsys.structures.b_factor, to_unit="angstrom**2"),
        [[20] * 4],
    )


def test_tree_is_separate_explicit_evidence_with_correct_index_axis(tmp_path):
    path = tmp_path / "ligand.pdbqt"
    path.write_text(LIGAND)
    tree = get_torsion_tree(path)
    assert tree["atom_ids"].tolist() == ["17", "3", "45", "90"]
    assert tree["fragment_offsets"].tolist() == [0, 2, 4]
    assert tree["fragment_atom_indices"].tolist() == [0, 1, 2, 3]
    assert tree["branch_atom_pairs"].tolist() == [[0, 2]]
    assert tree["branch_fragment_pairs"].tolist() == [[0, 1]]
    assert tree["torsdof"] == 2  # Not inferred from the one active branch.
    with pytest.raises(FormatError, match="discard_torsion_tree"):
        msm.convert(path, to_form="molsysmt.MolSys")
    molsys = native(path)
    assert molsys.topology.bonds[["atom1_index", "atom2_index"]].values.tolist() == [
        [0, 2]
    ]
    assert msm.get(molsys, element="bond", bond_order=True) == [None]
    tree["branch_atom_pairs"][0, 0] = 1
    assert get_torsion_tree(path)["branch_atom_pairs"].tolist() == [[0, 2]]


def test_round_trip_preserves_supplied_tree_types_charges_hydrogens_and_source(
    source, tmp_path
):
    molsys = native(source)
    tree = get_torsion_tree(source)
    before_atoms = molsys.topology.atoms.copy()
    before_coords = msm.pyunitwizard.get_value(
        molsys.structures.coordinates, to_unit="nm"
    ).copy()
    output = tmp_path / "roundtrip.pdbqt"
    msm.convert(molsys, to_form=output, typing_scheme="autodock4", torsion_tree=tree)
    restored = native(output)
    assert (
        restored.topology.atoms.atom_id.tolist()
        == molsys.topology.atoms.atom_id.tolist()
    )
    np.testing.assert_array_equal(
        restored.molecular_mechanics.atom_ff_type,
        molsys.molecular_mechanics.atom_ff_type,
    )
    np.testing.assert_allclose(
        restored.molecular_mechanics.partial_charge.astype(float),
        molsys.molecular_mechanics.partial_charge.astype(float),
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        before_coords,
    )
    pd.testing.assert_frame_equal(molsys.topology.atoms, before_atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm"),
        before_coords,
    )
    restored_tree = get_torsion_tree(output)
    if tree is None:
        assert restored_tree is None
    else:
        for name, value in tree.items():
            np.testing.assert_equal(restored_tree[name], value)


def test_identity_bridge_preserves_crlf_remarks_and_tree_bytes(tmp_path):
    path = tmp_path / "source.pdbqt"
    payload = LIGAND.replace("\n", "\r\n").encode()
    path.write_bytes(payload)
    text, report = msm.convert(
        path, to_form="string:pdbqt_text", strict=True, return_report=True
    )
    assert not report.is_lossy and report.is_exhaustive
    output = tmp_path / "copy.pdbqt"
    msm.convert(text, to_form=output, strict=True)
    assert output.read_bytes() == payload


def test_explicit_complete_indices_are_an_identity_projection(tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(LIGAND)
    text, report = msm.convert(
        path,
        to_form="string:pdbqt_text",
        selection=[3, 2, 1, 0],
        structure_indices=[0],
        strict=True,
        return_report=True,
    )
    assert text == "pdbqt_text:" + LIGAND
    assert report.is_exhaustive and not report.is_lossy


def test_nested_and_sibling_branches_round_trip(tmp_path):
    branch = "\n".join(
        [
            "ROOT",
            ATOMS[0],
            "ENDROOT",
            "BRANCH 17 3",
            ATOMS[1],
            "BRANCH 3 90",
            ATOMS[3],
            "ENDBRANCH 3 90",
            "ENDBRANCH 17 3",
            "BRANCH 17 45",
            ATOMS[2],
            "ENDBRANCH 17 45",
            "TORSDOF 3",
            "",
        ]
    )
    path = tmp_path / "nested.pdbqt"
    path.write_text(branch)
    tree = get_torsion_tree(path)
    assert tree["branch_fragment_pairs"].tolist() == [[0, 1], [1, 2], [0, 3]]
    assert tree["branch_atom_pairs"].tolist() == [[0, 1], [1, 2], [0, 3]]
    payload = msm.convert(
        native(path),
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=tree,
    )
    from molsysmt.form.string_pdbqt_text import get_torsion_tree as text_tree

    restored = text_tree(payload)
    for name, value in tree.items():
        np.testing.assert_equal(restored[name], value)


def test_root_without_branches_keeps_declared_ligand_layout(tmp_path):
    path = tmp_path / "root.pdbqt"
    path.write_text("\n".join(["ROOT", *ATOMS, "ENDROOT", "TORSDOF 0", ""]))
    tree = get_torsion_tree(path)
    assert tree["branch_atom_pairs"].shape == (0, 2)
    payload = msm.convert(
        native(path),
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=tree,
    )
    assert "ROOT\n" in payload and "TORSDOF 0\n" in payload


@pytest.mark.parametrize(
    "defect", ["offsets", "duplicate_atom", "endpoint", "cycle", "dtype", "torsdof"]
)
def test_invalid_supplied_tree_does_not_touch_destination(defect, tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(LIGAND)
    molsys = native(path)
    tree = get_torsion_tree(path)
    if defect == "offsets":
        tree["fragment_offsets"] = np.array([0, 0, 4])
    elif defect == "duplicate_atom":
        tree["fragment_atom_indices"][0] = 1
    elif defect == "endpoint":
        tree["branch_atom_pairs"][0, 1] = 5
    elif defect == "cycle":
        tree["branch_fragment_pairs"][0] = [1, 1]
        tree["branch_atom_pairs"][0] = [2, 3]
    elif defect == "dtype":
        tree["branch_atom_pairs"] = tree["branch_atom_pairs"].astype(float)
    else:
        tree["torsdof"] = True
    output = tmp_path / "output.pdbqt"
    output.write_text("keep")
    with pytest.raises(FormatError):
        msm.convert(
            molsys, to_form=output, typing_scheme="autodock4", torsion_tree=tree
        )
    assert output.read_text() == "keep"


def test_loss_report_and_strict_mode_fail_before_output(tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(LIGAND)
    report = msm.get_conversion_report(path, to_form="molsysmt.MolSys")
    assert {"pdbqt_torsion_tree", "pdbqt_remarks"} <= {
        issue.attribute for issue in report.issues
    }
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(
            path, to_form="molsysmt.MolSys", strict=True, discard_torsion_tree=True
        )
    output = tmp_path / "untouched.pdbqt"
    output.write_text("keep")
    with pytest.raises(NotCompatibleConversionError):
        msm.convert(
            native(path), to_form=output, strict=True, typing_scheme="autodock4"
        )
    assert output.read_text() == "keep"


def test_selection_and_explicit_structure_indices(source, tmp_path):
    selected = msm.convert(
        source,
        to_form="molsysmt.MolSys",
        selection=[3, 1],
        structure_indices=[0],
        discard_torsion_tree=True,
    )
    assert selected.topology.atoms.atom_id.tolist() == ["3", "90"]
    np.testing.assert_array_equal(
        selected.molecular_mechanics.atom_ff_type, ["A", "HD"]
    )
    for indices in ([1], [-1]):
        with pytest.raises(ArgumentError):
            msm.convert(
                source,
                to_form="molsysmt.MolSys",
                structure_indices=indices,
                discard_torsion_tree=True,
            )
    if get_torsion_tree(source) is not None:
        with pytest.raises(FormatError, match="remapped"):
            msm.convert(source, to_form=tmp_path / "subset.pdbqt", selection=[0, 1])
        with pytest.raises(FormatError, match="atom_ids"):
            msm.convert(
                selected,
                to_form="string:pdbqt_text",
                typing_scheme="autodock4",
                torsion_tree=get_torsion_tree(source),
            )
    else:
        output = msm.convert(source, to_form="string:pdbqt_text", selection=[3, 1])
        assert native(output).topology.atoms.atom_id.tolist() == ["3", "90"]


@pytest.mark.parametrize(
    "payload",
    [
        LIGAND.replace("ENDBRANCH 17 45", "ENDBRANCH 3 45"),
        LIGAND.replace("ENDBRANCH 17 45\n", ""),
        LIGAND.replace("TORSDOF 2", "TORSDOF -1"),
        LIGAND.replace("TORSDOF 2", "TORSDOF 2\nTORSDOF 2"),
        LIGAND.replace("BRANCH 17 45", "BRANCH 17 3"),
        LIGAND.replace("ROOT\n", "ROOT\nROOT\n", 1),
        "MODEL 1\n" + RIGID,
        "BEGIN_RES LIG 1\n" + RIGID,
        RIGID.replace(" HD", " G0"),
        RIGID.replace(" OA", " W"),
        RIGID.replace(" 0.125 C", "       C"),
        RIGID.replace(" 0.125 C", "   nan C"),
        RIGID.replace("   1.000", "     nan", 1),
        RIGID.replace("ATOM      3", "ATOM     17"),
    ],
)
def test_invalid_and_unsupported_records_fail(payload, tmp_path):
    path = tmp_path / "invalid.pdbqt"
    path.write_text(payload)
    with pytest.raises(FormatError):
        native(path)


@pytest.mark.parametrize(
    "defect",
    ["scheme", "charge", "types", "element", "serial", "isotope", "coordinate"],
)
def test_writer_errors_do_not_touch_existing_destination(defect, tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(RIGID)
    molsys = native(path)
    scheme = "autodock4"
    if defect == "scheme":
        scheme = None
    elif defect == "charge":
        molsys.molecular_mechanics.atoms_ff.loc[0, "partial_charge"] = np.nan
    elif defect == "types":
        molsys.molecular_mechanics.atoms_ff.loc[0, "atom_ff_type"] = "G0"
    elif defect == "element":
        molsys.topology.atoms.loc[0, "atom_type"] = "N"
    elif defect == "serial":
        molsys.topology.atoms.loc[0, "atom_id"] = "carbon"
    elif defect == "isotope":
        molsys.topology.atoms.loc[0, "isotope"] = 13
    else:
        molsys.structures.coordinates = msm.pyunitwizard.quantity(
            np.full((1, 4, 3), np.nan), "nm"
        )
    output = tmp_path / "output.pdbqt"
    output.write_text("keep")
    with pytest.raises(FormatError):
        msm.convert(molsys, to_form=output, typing_scheme=scheme)
    assert output.read_text() == "keep"


def test_explicit_angstrom_boundary_under_nondefault_unit_policy(tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(RIGID)
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        molsys = native(path)
        payload = msm.convert(
            molsys, to_form="string:pdbqt_text", typing_scheme="autodock4"
        )
        restored = native(payload)
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                restored.structures.coordinates, to_unit="angstrom"
            )[0, 0],
            [1, 2, 3],
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                restored.structures.b_factor, to_unit="angstrom**2"
            ),
            [[20] * 4],
        )


@pytest.mark.skipif(
    importlib.util.find_spec("MDAnalysis") is None,
    reason="optional independent PDBQT reader",
)
def test_atom_fields_against_independent_reader(source):
    import MDAnalysis as mda

    reference = mda.Universe(str(source))
    molsys = native(source)
    np.testing.assert_array_equal(
        reference.atoms.ids.astype(str), molsys.topology.atoms.atom_id
    )
    np.testing.assert_array_equal(
        reference.atoms.types, molsys.molecular_mechanics.atom_ff_type
    )
    np.testing.assert_allclose(
        reference.atoms.charges,
        molsys.molecular_mechanics.partial_charge.astype(float),
        atol=1e-7,
    )
    np.testing.assert_allclose(
        reference.atoms.positions,
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="angstrom")[
            0
        ],
        atol=1e-6,
    )


def test_complete_native_graph_must_agree_with_supplied_tree(tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(LIGAND)
    molsys = native(path)
    molsys.topology.bonds = pd.DataFrame(
        {
            "atom1_index": [0, 0, 2],
            "atom2_index": [1, 2, 3],
            "bond_type": ["covalent"] * 3,
        }
    )
    molsys.chemical_states._states[0].connectivity_completeness = "complete"
    tree = get_torsion_tree(path)
    msm.convert(
        molsys,
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=tree,
    )
    bad = copy.deepcopy(tree)
    bad["fragment_atom_indices"] = np.asarray([0, 3, 1, 2], dtype=np.int64)
    with pytest.raises(FormatError, match="fragments must agree"):
        msm.convert(
            molsys,
            to_form="string:pdbqt_text",
            typing_scheme="autodock4",
            torsion_tree=bad,
        )


def test_tree_writer_accepts_unavailable_chemistry_without_claiming_a_complete_graph(
    tmp_path,
):
    path = tmp_path / "source.pdbqt"
    path.write_text(LIGAND)
    molsys = native(path)
    molsys.chemical_states = msm.ChemicalStates(n_atoms=4)
    payload = msm.convert(
        molsys,
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=get_torsion_tree(path),
    )
    assert (
        native(payload).chemical_states._states[0].connectivity_completeness
        == "partial"
    )


@pytest.mark.parametrize("indices", [[-1], [4], []])
def test_direct_mechanical_getters_validate_atom_axis(indices, tmp_path):
    path = tmp_path / "source.pdbqt"
    path.write_text(RIGID)
    from molsysmt.form.file_pdbqt import get_partial_charge_from_atom

    if indices:
        with pytest.raises(ArgumentError):
            get_partial_charge_from_atom(path, indices=indices)
    else:
        assert get_partial_charge_from_atom(path, indices=indices).shape == (0,)


def test_shared_molsys_pipe_also_preserves_mechanical_fields(tmp_path, monkeypatch):
    from molsysmt.form import file_pdbqt as adapter

    path = tmp_path / "rigid.pdbqt"
    path.write_text(RIGID)
    monkeypatch.setattr(adapter, "piped_any_attribute", "molsysmt.MolSys")
    output = msm.get(
        path,
        element="atom",
        atom_type=True,
        atom_ff_type=True,
        partial_charge=True,
        coordinates=True,
        output_type="dictionary",
    )
    np.testing.assert_array_equal(output["atom_ff_type"], ["C", "A", "OA", "HD"])
    np.testing.assert_allclose(output["partial_charge"], [0.125, -0.1, -0.25, 0.225])
    assert output["coordinates"].shape == (1, 4, 3)
