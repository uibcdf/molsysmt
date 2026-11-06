"""Check prepared-field fidelity against independent fixed-column observations."""

import copy
import json
from hashlib import sha256

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    FormatError,
    MemoryBudgetExceededError,
)
from molsysmt.native import PDBQTFileHandler
from tests.form.file_pdbqt.test_native_contract import ATOMS, LIGAND, RIGID

PAIRS = [[0, 2], [1, 0], [2, 3], [3, 1]]
XYZ = np.array([[31.1234, 32, 33], [11, 12, 13], [41, 42, 43], [21, 22, 23]])


def atoms(payload):
    return [
        line
        for line in payload.removeprefix("pdbqt_text:").splitlines()
        if line.startswith(("ATOM  ", "HETATM"))
    ]


def run(source, route, tmp_path, coordinates=None, **kwargs):
    coordinates = (
        msm.pyunitwizard.quantity(XYZ, "angstrom")
        if coordinates is None
        else coordinates
    )
    kwargs.setdefault("atom_correspondence", PAIRS)
    if route == "text":
        msm.get_form("pdbqt_text:" + source)
        return msm.form.string_pdbqt_text.project_coordinates(
            "pdbqt_text:" + source, coordinates, **kwargs
        )
    path = tmp_path / "source.pdbqt"
    path.write_bytes(source.encode("utf-8"))
    if route == "file":
        msm.get_form(path)
        return msm.form.file_pdbqt.project_coordinates(path, coordinates, **kwargs)
    with PDBQTFileHandler(path, storage_mode=route) as handler:
        return handler.project_coordinates(coordinates, **kwargs)


@pytest.mark.parametrize("route", ["text", "file", "resident", "indexed"])
@pytest.mark.parametrize("source", [RIGID, LIGAND])
def test_projection_preserves_prepared_fields_and_known_nonidentity_map(
    route, source, tmp_path
):
    source = source.replace(ATOMS[0][68:76], "0.123456", 1).replace(
        "ATOM  ", "HETATM", 1
    )
    before = source
    provenance = {"state": "caller:fixed-1", "evidence": ["declared"]}
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        result = run(
            source,
            route,
            tmp_path,
            discard_remarks=True,
            chemical_state_provenance=provenance,
        )
        assert (
            msm.pyunitwizard.has_unit(
                msm.pyunitwizard.standardize(msm.pyunitwizard.quantity(1, "angstrom")),
                "pm",
            )
            is True
        )
    report = result["report"]
    written = result["molecular_system"]
    before_atoms, after_atoms = atoms(source), atoms(written)
    for original, changed in zip(before_atoms, after_atoms, strict=True):
        assert original[:30] == changed[:30]
        assert original[54:] == changed[54:]
    assert after_atoms[0][68:76] == "0.123456"
    actual_xyz = [
        [float(line[i : i + 8]) for i in (30, 38, 46)] for line in after_atoms
    ]
    np.testing.assert_allclose(actual_xyz, XYZ[[1, 3, 0, 2]], rtol=0, atol=0.0005)
    assert source == before
    assert report["schema_version"] == "molsysmt.pdbqt_coordinate_projection@1"
    assert report["source_payload"]["sha256"] == sha256(source.encode()).hexdigest()
    assert (
        report["output_payload"]["sha256"] == sha256(written[11:].encode()).hexdigest()
    )
    assert report["source_payload"]["n_bytes"] == len(source.encode())
    assert report["output_payload"]["n_bytes"] == len(written[11:].encode())
    assert report["coordinate_to_source_atom_indices"] == [2, 0, 3, 1]
    assert report["output_to_coordinate_atom_indices"] == [1, 3, 0, 2]
    assert report["output_to_source_atom_indices"] == [0, 1, 2, 3]
    assert report["output_to_source_structure_indices"] == [0]
    assert report["source_structure_ids"] == [None]
    assert report["coordinate_precision"]["unit"] == "angstrom"
    np.testing.assert_allclose(
        report["coordinate_precision"]["max_absolute_error"], [0.0004], atol=1e-12
    )
    assert report["chemical_state_provenance"] == provenance
    provenance["evidence"].append("later")
    assert report["chemical_state_provenance"]["evidence"] == ["declared"]
    json.dumps(report, allow_nan=False)
    native = msm.convert(written, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    assert native.chemical_states._states[0].connectivity_completeness == "partial"
    assert native.topology.atoms.atom_id.tolist() == ["17", "3", "45", "90"]
    if source == LIGAND or "ROOT" in source:
        original = msm.form.string_pdbqt_text.get_torsion_tree("pdbqt_text:" + source)
        projected = msm.form.string_pdbqt_text.get_torsion_tree(written)
        for key in original:
            np.testing.assert_array_equal(original[key], projected[key])


def model_source():
    return "\n".join(
        [
            "REMARK global preparation",
            *(
                f"MODEL {label}\nREMARK VINA RESULT: -1.2 0 0\n{RIGID}ENDMDL"
                for label in ("009", "2", "51")
            ),
            "REMARK trailing score",
            "END",
            "",
        ]
    )


@pytest.mark.parametrize("route", ["text", "file", "resident", "indexed"])
def test_reordered_nonconsecutive_models_keep_source_labels_and_coordinate_order(
    route, tmp_path
):
    xyz = np.stack([XYZ, XYZ + 100])
    result = run(
        model_source(),
        route,
        tmp_path,
        coordinates=msm.pyunitwizard.quantity(xyz / 10, "nm"),
        structure_indices=[2, 0],
        discard_remarks=True,
    )
    report = result["report"]
    assert report["output_to_source_structure_indices"] == [2, 0]
    assert report["source_structure_ids"] == ["51", "009"]
    assert report["metadata_disposition"]["discarded_remark_count"] == 5
    text = result["molecular_system"]
    assert "REMARK" not in text
    assert [
        line
        for line in text.removeprefix("pdbqt_text:").splitlines()
        if line.startswith("MODEL")
    ] == [
        "MODEL 51",
        "MODEL 009",
    ]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(msm.get(text, coordinates=True), to_unit="angstrom"),
        xyz[:, [1, 3, 0, 2]],
        rtol=0,
        atol=0.0005,
    )


@pytest.mark.parametrize("route", ["text", "file", "resident", "indexed"])
def test_all_remarks_require_explicit_disposition_even_outside_selected_model(
    route, tmp_path
):
    source = "MODEL 3\n" + RIGID + "ENDMDL\nREMARK VINA RESULT: -9 0 0\n"
    target = tmp_path / "output.pdbqt"
    target.write_bytes(b"existing destination")
    with pytest.raises(FormatError, match="discard_remarks"):
        run(source, route, tmp_path, structure_indices=0, output_filename=target)
    assert target.read_bytes() == b"existing destination"


@pytest.mark.parametrize(
    "pairs",
    [
        [[0, 0], [1, 1], [2, 2]],
        [[0, 0], [1, 1], [2, 2], [3, 2]],
        [[0, 0], [1, 1], [2, 2], [3, 5]],
        [[0, 0], [1, 1], [2, 2], [-1, 3]],
        [[0, 0], [1, 1], [2, 2], [True, 3]],
        [[0.0, 0], [1, 1], [2, 2], [3, 3]],
        np.array([[0, 0], [1, 1], [2, 2], [3, 2**63]], dtype=np.uint64),
    ],
)
def test_incomplete_ambiguous_or_nonpositional_maps_are_refused(pairs, tmp_path):
    with pytest.raises(ArgumentError):
        run(RIGID, "text", tmp_path, atom_correspondence=pairs)


@pytest.mark.parametrize("unit", [None, "ps", "dimensionless", "angstrom**2"])
def test_coordinates_require_explicit_length_units(unit, tmp_path):
    value = XYZ if unit is None else msm.pyunitwizard.quantity(XYZ, unit)
    with pytest.raises(ArgumentError):
        run(RIGID, "text", tmp_path, coordinates=value)


@pytest.mark.parametrize(
    "value",
    [
        np.ones((3, 3)),
        np.ones((2, 4, 3)),
        np.ones((4, 4)),
        np.ones((4, 3), dtype=complex) * (1 + 2j),
        np.ones((4, 3), dtype=bool),
    ],
)
def test_incompatible_coordinate_axes_or_nonreal_values_are_refused(value, tmp_path):
    with pytest.raises(ArgumentError):
        run(RIGID, "text", tmp_path, coordinates=msm.pyunitwizard.quantity(value, "nm"))


@pytest.mark.parametrize("unit", ["dimensionless", "nm"])
def test_quantity_wrapped_atom_maps_are_not_positional_indices(unit, tmp_path):
    with pytest.raises(ArgumentError):
        run(
            RIGID,
            "text",
            tmp_path,
            atom_correspondence=msm.pyunitwizard.quantity(PAIRS, unit),
        )


@pytest.mark.parametrize(
    "provenance",
    [
        [],
        {"state": np.nan},
        {"state": object()},
        {1: "state"},
        {"1": "one", 1: "other"},
        {"states": [{1: "state"}]},
    ],
)
def test_provenance_requires_a_json_compatible_declaration(provenance, tmp_path):
    with pytest.raises(ArgumentError):
        run(RIGID, "text", tmp_path, chemical_state_provenance=provenance)


@pytest.mark.parametrize("indices", [[], [0, 0], [3], [True], [0.0]])
def test_invalid_structure_selections_are_refused(indices, tmp_path):
    with pytest.raises(ArgumentError):
        run(RIGID, "text", tmp_path, structure_indices=indices)


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf, 10000, -1000])
def test_adverse_later_coordinates_do_not_publish_partial_file(value, tmp_path):
    xyz = np.stack([XYZ, XYZ])
    xyz[1, 3, 2] = value
    target = tmp_path / "output.pdbqt"
    target.write_bytes(b"existing destination")
    with pytest.raises(FormatError, match="finite|8.3"):
        run(
            model_source(),
            "file",
            tmp_path,
            coordinates=msm.pyunitwizard.quantity(xyz, "angstrom"),
            structure_indices=[0, 2],
            output_filename=target,
            discard_remarks=True,
        )
    assert target.read_bytes() == b"existing destination"
    assert list(tmp_path.glob(".molsysmt-pdbqt-*")) == []


@pytest.mark.parametrize("mode", ["resident", "indexed"])
@pytest.mark.parametrize("alias", ["same", "symlink", "hardlink"])
def test_source_alias_paths_and_copied_handlers_never_overwrite_source(
    mode, alias, tmp_path
):
    path = tmp_path / "source.pdbqt"
    path.write_bytes(RIGID.encode())
    target = path if alias == "same" else tmp_path / "alias.pdbqt"
    if alias == "symlink":
        try:
            target.symlink_to(path)
        except OSError:
            pytest.skip("Host does not permit symbolic links")
    elif alias == "hardlink":
        target.hardlink_to(path)
    with PDBQTFileHandler(path, storage_mode=mode) as handler, handler.copy() as copied:
        with pytest.raises(ArgumentError, match="different file"):
            copied.project_coordinates(
                msm.pyunitwizard.quantity(XYZ, "angstrom"),
                PAIRS,
                output_filename=target,
            )
    assert path.read_bytes() == RIGID.encode()


def test_nested_tree_and_noncoordinate_columns_survive_without_complete_chemistry(
    tmp_path,
):
    source = LIGAND.replace(
        ATOMS[3] + "\nENDBRANCH 17 45",
        "BRANCH 45 90\n" + ATOMS[3] + "\nENDBRANCH 45 90\nENDBRANCH 17 45",
    )
    result = run(source, "text", tmp_path, discard_remarks=True)
    expected = [
        line
        for line in source.splitlines()
        if line.split()[:1]
        in (["ROOT"], ["ENDROOT"], ["BRANCH"], ["ENDBRANCH"], ["TORSDOF"])
    ]
    actual = [
        line
        for line in result["molecular_system"].removeprefix("pdbqt_text:").splitlines()
        if line.split()[:1]
        in (["ROOT"], ["ENDROOT"], ["BRANCH"], ["ENDBRANCH"], ["TORSDOF"])
    ]
    assert actual == expected


def test_indexed_file_projection_does_not_materialize_whole_payload(
    tmp_path, monkeypatch
):
    source = tmp_path / "source.pdbqt"
    source.write_text(model_source())
    with PDBQTFileHandler(source, storage_mode="indexed") as handler:

        def forbidden(_self):
            raise AssertionError("whole source materialized")

        monkeypatch.setattr(type(handler._document), "payload", property(forbidden))
        before = copy.deepcopy(handler._document.first)
        for i in range(3):
            target = tmp_path / f"projected-{i}.pdbqt"
            result = handler.project_coordinates(
                msm.pyunitwizard.quantity(XYZ + i, "angstrom"),
                PAIRS,
                structure_indices=[2],
                output_filename=target,
                discard_remarks=True,
            )
            assert result["molecular_system"] == str(target)
            assert (
                result["report"]["output_payload"]["sha256"]
                == sha256(target.read_bytes()).hexdigest()
            )
            assert len(atoms(target.read_text())) == 4
        assert handler._document.first == before
    assert source.read_text() == model_source()


def test_changed_indexed_source_is_refused(tmp_path):
    source = tmp_path / "source.pdbqt"
    source.write_text(RIGID)
    with PDBQTFileHandler(source, storage_mode="indexed") as handler:
        source.write_text(RIGID + "\n")
        with pytest.raises(FormatError, match="changed"):
            handler.project_coordinates(
                msm.pyunitwizard.quantity(XYZ, "angstrom"), PAIRS
            )


def test_adverse_unselected_source_model_is_validated_before_output(tmp_path):
    source = model_source().replace("MODEL 51", "MODEL 9")
    target = tmp_path / "output.pdbqt"
    target.write_bytes(b"unchanged")
    with pytest.raises(FormatError, match="Repeated"):
        run(
            source,
            "file",
            tmp_path,
            structure_indices=[0],
            output_filename=target,
            discard_remarks=True,
        )
    assert target.read_bytes() == b"unchanged"


def test_non_ascii_model_labels_are_rejected_before_projection(tmp_path):
    with pytest.raises(FormatError, match="MODEL"):
        run("MODEL ９\n" + RIGID + "ENDMDL\n", "text", tmp_path)


def test_budget_distinguishes_full_text_from_one_model_file_buffers(
    tmp_path, monkeypatch
):
    source = "".join(f"MODEL {i + 1}\n{RIGID}ENDMDL\n" for i in range(100))
    xyz = msm.pyunitwizard.quantity(np.repeat(XYZ[None, ...], 100, axis=0), "angstrom")
    monkeypatch.setattr(msm.configure, "max_ram_usage", 12_000)
    with pytest.raises(MemoryBudgetExceededError):
        run(source, "file", tmp_path, coordinates=xyz)
    target = tmp_path / "bounded.pdbqt"
    result = run(source, "file", tmp_path, coordinates=xyz, output_filename=target)
    assert len(atoms(target.read_text())) == 400
    assert result["report"]["execution"]["output"] == "streamed_file"


def test_payload_hash_and_remark_policy_cover_unicode_crlf_and_chunk_boundaries(
    tmp_path,
):
    source = "REMARK " + "é" * 40_000 + "\r\n" + RIGID.replace("\n", "\r\n")
    result = run(source, "file", tmp_path, discard_remarks=True)
    assert (
        result["report"]["source_payload"]["sha256"]
        == sha256(source.encode()).hexdigest()
    )
    assert result["report"]["metadata_disposition"]["discarded_remark_count"] == 1
    assert len(atoms(result["molecular_system"])) == 4


def test_unchanged_source_coordinates_and_input_array_after_projection(tmp_path):
    xyz = XYZ.copy()
    pairs = np.asarray(PAIRS)
    with PDBQTFileHandler("pdbqt_text:" + RIGID) as handler:
        before = handler.get_coordinates()
        handler.project_coordinates(msm.pyunitwizard.quantity(xyz, "nm"), pairs)
        np.testing.assert_array_equal(xyz, XYZ)
        np.testing.assert_array_equal(pairs, PAIRS)
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(handler.get_coordinates(), to_unit="nm"),
            msm.pyunitwizard.get_value(before, to_unit="nm"),
        )


@pytest.mark.parametrize(
    "case", ["1iep", "1s63", "5x72-p59", "5x72-p69", "1iep-receptor"]
)
def test_pinned_real_preparations_retain_fields_under_mapped_coordinate_projection(
    case, vina_reference_corpus, tmp_path
):
    root, records = vina_reference_corpus
    source = root / records[case]["files"]["pdbqt"]["filename"]
    original_bytes = source.read_bytes()
    original_atoms = atoms(original_bytes.decode())
    original_xyz = np.asarray(
        [[float(line[i : i + 8]) for i in (30, 38, 46)] for line in original_atoms]
    )
    replacement = original_xyz + [0.1, -0.2, 0.3]
    n = len(original_atoms)
    pairs = np.column_stack([np.arange(n), np.arange(n)[::-1]])
    target = tmp_path / "conformation.pdbqt"
    msm.get_form(source)
    result = msm.form.file_pdbqt.project_coordinates(
        source,
        msm.pyunitwizard.quantity(replacement[::-1], "angstrom"),
        pairs,
        output_filename=target,
        discard_remarks=True,
    )
    projected_atoms = atoms(target.read_text())
    assert len(projected_atoms) == n
    for original, projected in zip(original_atoms, projected_atoms, strict=True):
        assert projected[:30] == original[:30]
        assert projected[54:] == original[54:]
    actual = [
        [float(line[i : i + 8]) for i in (30, 38, 46)] for line in projected_atoms
    ]
    np.testing.assert_allclose(actual, replacement, rtol=0, atol=0.0005)
    assert source.read_bytes() == original_bytes
    assert (
        result["report"]["source_payload"]["sha256"]
        == sha256(original_bytes).hexdigest()
    )


def test_ready_projection_loads_no_optional_chemical_engine():
    import subprocess
    import sys

    script = r"""
import importlib.abc
import importlib.machinery
import sys
import molsysmt as msm
from molsysmt.native import PDBQTFileHandler
roots = {"rdkit", "meeko", "openmm", "MDAnalysis", "mdtraj", "vina"}
assert not roots.intersection(name.split(".")[0] for name in sys.modules)
attempted = []
class DeniedLoader(importlib.abc.Loader):
    def create_module(self, spec):
        attempted.append(spec.name)
        raise ImportError("unexpected optional engine: " + spec.name)
    def exec_module(self, module):
        raise AssertionError("unexpected engine execution")
class DeniedEngines(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in roots:
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            if spec is not None:
                spec.loader = DeniedLoader()
            return spec
sys.meta_path.insert(0, DeniedEngines())
with PDBQTFileHandler("pdbqt_text:" + sys.argv[1]) as handler:
    result = handler.project_coordinates(
        msm.pyunitwizard.quantity([[1,2,3],[2,3,4],[3,4,5],[4,5,6]], "angstrom"),
        [[0,0],[1,1],[2,2],[3,3]])
assert result["report"]["output_to_source_atom_indices"] == [0,1,2,3]
assert not attempted, attempted
assert not roots.intersection(name.split(".")[0] for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", script, RIGID],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
