"""Protecting source and bundled MET graphs against undeclared endpoints."""

import gzip
import hashlib
import json
import pickle
from pathlib import Path

import pytest

import molsysmt as msm

DATABASE = Path(msm.__file__).parent / "data" / "databases" / "amino_acids"
EXTRA = DATABASE / "extra.json"

# AmberClassic aminont12.lib, NMET: only intra-group connectivity is represented.
# Reference commit: 656e5c6fcb05149e6aa936e1d69d1426b37ea3c7.
EXPECTED_PAIRS = [
    ["N", "CA"],
    ["N", "H1"],
    ["N", "H2"],
    ["N", "H3"],
    ["CA", "C"],
    ["CA", "CB"],
    ["CA", "HA"],
    ["C", "O"],
    ["CB", "CG"],
    ["CB", "HB2"],
    ["CB", "HB3"],
    ["CG", "SD"],
    ["CG", "HG2"],
    ["CG", "HG3"],
    ["SD", "CE"],
    ["CE", "HE1"],
    ["CE", "HE2"],
    ["CE", "HE3"],
]


def _expected(first_hydrogen):
    return [
        [first_hydrogen if atom == "H1" else atom for atom in pair]
        for pair in EXPECTED_PAIRS
    ]


def test_all_amino_acid_supplements_have_declared_endpoints():
    for group, record in json.loads(EXTRA.read_text()).items():
        for variant in record["topology"]:
            assert {atom for pair in variant["bonds"] for atom in pair} <= set(
                variant["atoms"]
            ), group


@pytest.mark.parametrize("first_hydrogen,index", [("H1", 4), ("H", 5)])
def test_bundled_and_source_met_have_reference_n_terminal_graph(first_hydrogen, index):
    source = json.loads(EXTRA.read_text())["MET"]["topology"][index - 4]
    bundled = msm.element.group.amino_acid.get_group_db("MET")["topology"][index]
    expected = {frozenset(pair) for pair in _expected(first_hydrogen)}
    assert source == bundled
    assert {frozenset(pair) for pair in bundled["bonds"]} == expected
    assert len(bundled["atoms"]) == 19 and len(bundled["bonds"]) == 18
    assert "OXT" not in bundled["atoms"]


@pytest.mark.parametrize("first_hydrogen,index", [("H1", 4), ("H", 5)])
def test_met_reader_retains_graph_with_reordered_external_indices(
    first_hydrogen, index
):
    atoms = msm.element.group.amino_acid.get_group_db("MET")["topology"][index]["atoms"]
    names = list(reversed(atoms))
    indices = list(range(107, 107 + 3 * len(names), 3))
    by_name = dict(zip(names, indices))
    expected = sorted(
        sorted([by_name[a], by_name[b]]) for a, b in _expected(first_hydrogen)
    )
    assert (
        msm.element.group.amino_acid.get_bonded_atom_pairs(
            "MET", names, atom_indices=indices
        )
        == expected
    )


def test_met_ccd_variants_still_include_terminal_oxygen():
    variants = msm.element.group.amino_acid.get_group_db("MET")["topology"]
    assert len(variants) == 6
    for variant in variants[:2]:
        assert "OXT" in variant["atoms"]
        assert frozenset(["C", "OXT"]) in {frozenset(pair) for pair in variant["bonds"]}


def test_corrected_supplement_can_be_used_by_ccd_generator(tmp_path):
    from molsysmt.data._make._chemical_group_database import _main

    ccd = Path(__file__).parent / "data" / "mini_ccd.cif"
    output = tmp_path / "references"
    assert (
        _main(
            "amino_acids",
            ["--ccd", str(ccd), "--extra", str(EXTRA), "--output-dir", str(output)],
        )
        == 0
    )
    with gzip.open(output / "M.pkl.gz", "rb") as stream:
        generated = pickle.load(stream)
    assert (
        generated["MET"]["topology"] == json.loads(EXTRA.read_text())["MET"]["topology"]
    )


@pytest.fixture
def revision_inputs(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    original = {"atoms": ["N", "C"], "bonds": [["N", "C"], ["C", "OXT"]]}
    replacement = {"atoms": ["N", "C"], "bonds": [["N", "C"]]}
    previous = {"MET": {"name": "MET", "topology": [original]}}
    revised = {"MET": {"name": "MET", "topology": [replacement]}}
    before, after = tmp_path / "previous.json", tmp_path / "revised.json"
    before.write_text(json.dumps(previous))
    after.write_text(json.dumps(revised))
    records = {
        "MET": {
            "name": "METHIONINE",
            "topology": [{"atoms": ["C", "O"], "bonds": [["C", "O"]]}, original],
        },
        "MKEEP": {
            "name": "retained reference",
            "topology": [{"atoms": ["X"], "bonds": []}],
        },
    }
    with gzip.open(source / "M.pkl.gz", "wb") as stream:
        pickle.dump(records, stream)
    return source, before, after, records


def _revise(inputs, output):
    from molsysmt.data._make.revise_amino_acid_supplements import _main

    source, before, after, _ = inputs
    return _main(
        [
            "--source-dir",
            str(source),
            "--previous-extra",
            str(before),
            "--extra",
            str(after),
            "--output-dir",
            str(output),
        ]
    )


def test_revision_preserves_unaffected_records_and_source_bytes(
    tmp_path, revision_inputs
):
    source, before, after, records = revision_inputs
    input_bytes = {
        path: path.read_bytes() for path in [source / "M.pkl.gz", before, after]
    }
    output = tmp_path / "revised"
    assert _revise(revision_inputs, output) == 0
    with gzip.open(output / "M.pkl.gz", "rb") as stream:
        generated = pickle.load(stream)
    assert generated.keys() == records.keys()
    assert generated["MKEEP"] == records["MKEEP"]
    assert generated["MET"]["name"] == "METHIONINE"
    assert generated["MET"]["topology"][0] == records["MET"]["topology"][0]
    assert generated["MET"]["topology"][1] == {
        "atoms": ["N", "C"],
        "bonds": [["N", "C"]],
    }
    assert sorted(path.name for path in output.iterdir()) == [
        "M.pkl.gz",
        "generation_manifest.json",
    ]
    for path, data in input_bytes.items():
        assert path.read_bytes() == data


def test_revision_records_hashes_and_is_byte_reproducible(tmp_path, revision_inputs):
    outputs = [tmp_path / "first", tmp_path / "second"]
    for output in outputs:
        assert _revise(revision_inputs, output) == 0
    files = [
        {path.name: path.read_bytes() for path in output.iterdir()}
        for output in outputs
    ]
    assert files[0] == files[1]
    manifest = json.loads(files[0]["generation_manifest.json"])
    assert manifest["changed_variant_indices"] == {"MET": [1]}
    source, before, after, _ = revision_inputs
    for record, path in zip(manifest["inputs"], [before, after, source / "M.pkl.gz"]):
        assert record["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert manifest["outputs"] == {
        "M.pkl.gz": hashlib.sha256(files[0]["M.pkl.gz"]).hexdigest()
    }


@pytest.mark.parametrize(
    "defect",
    [
        "unmatched",
        "ambiguous",
        "invalid_revision",
        "group_membership",
        "variant_count",
        "metadata",
    ],
)
def test_invalid_revision_does_not_publish_partial_output(
    tmp_path, revision_inputs, defect
):
    source, _, after, records = revision_inputs
    if defect in {"unmatched", "ambiguous"}:
        variants = records["MET"]["topology"]
        if defect == "unmatched":
            variants.pop()
        else:
            variants.append(variants[-1])
        with gzip.open(source / "M.pkl.gz", "wb") as stream:
            pickle.dump(records, stream)
    else:
        extra = json.loads(after.read_text())
        if defect == "invalid_revision":
            extra["MET"]["topology"][0]["bonds"].append(["C", "MISSING"])
        elif defect == "group_membership":
            extra["NEW"] = extra["MET"]
        elif defect == "variant_count":
            extra["MET"]["topology"].append(extra["MET"]["topology"][0])
        elif defect == "metadata":
            extra["MET"]["name"] = "changed name"
        after.write_text(json.dumps(extra))
    output = tmp_path / "output"
    with pytest.raises(ValueError):
        _revise(revision_inputs, output)
    assert not output.exists()


def test_revision_preserves_existing_destination(tmp_path, revision_inputs):
    output = tmp_path / "output"
    output.mkdir()
    path = output / "M.pkl.gz"
    path.write_bytes(b"caller-owned reference")
    with pytest.raises(FileExistsError):
        _revise(revision_inputs, output)
    assert path.read_bytes() == b"caller-owned reference"
    assert list(output.iterdir()) == [path]


def test_bundled_revision_receipt_identifies_the_generated_bytes():
    manifest = json.loads((DATABASE / "supplement_revision_manifest.json").read_text())
    assert manifest["changed_variant_indices"] == {"MET": [4, 5]}
    assert manifest["outputs"] == {
        "M.pkl.gz": hashlib.sha256((DATABASE / "M.pkl.gz").read_bytes()).hexdigest()
    }
