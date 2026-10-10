"""Checking real multi-container CCD regeneration and legacy reader delivery."""

import gzip
import hashlib
import json
import pickle
import runpy
import subprocess
import sys
from pathlib import Path

import pytest

CCD = Path(__file__).parent / "data" / "mini_ccd.cif"
KINDS = ["amino_acids", "ions", "saccharides", "small_molecules"]
EXPECTED_NAMES = {
    "amino_acids": ["ALA"],
    "ions": ["NA", "SO4"],
    "saccharides": ["GLC"],
    "small_molecules": ["LIG"],
}


def _run(kind, output, *extra):
    command = [
        sys.executable,
        "-m",
        f"molsysmt.data.databases.{kind}.make_{kind}_db",
        "--ccd",
        str(CCD),
        "--output-dir",
        str(output),
        *extra,
    ]
    if kind == "amino_acids":
        command += ["--amino-acid-name", "ALA"]
    return subprocess.run(command, capture_output=True, text=True, check=False)


def _load(output, filename):
    with gzip.open(output / filename, "rb") as stream:
        return pickle.load(stream)


@pytest.mark.parametrize("kind", KINDS)
def test_cli_generates_selected_groups_with_expected_connectivity(tmp_path, kind):
    output = tmp_path / kind
    result = _run(kind, output)
    assert result.returncode == 0, result.stderr
    assert _load(output, "group_names.pkl.gz") == EXPECTED_NAMES[kind]
    code = EXPECTED_NAMES[kind][-1]
    record = _load(output, code[0] + ".pkl.gz")[code]
    if kind == "ions":
        assert record == {
            "name": "SULFATE ION",
            "three_letter_code": "SO4",
            "atom_name": [["S", "O1"], ["S", "O1"]],
            "bonds": [[0, 1]],
        }
        assert _load(output, "N.pkl.gz")["NA"]["atom_name"] == [["NA"], ["Na"]]
    else:
        atoms = ["N", "CA"] if kind == "amino_acids" else ["C1", "O1"]
        aliases = {"amino_acids": ["NT", "CA"], "small_molecules": ["1C", "1O"]}.get(
            kind, atoms
        )
        assert record["topology"] == [
            {"atoms": atoms, "bonds": [atoms]},
            {"atoms": aliases, "bonds": [aliases]},
        ]
    if kind == "saccharides":
        assert record["name"] == "EXAMPLE SUGAR\nwith a multiline name"
    assert not any(path.suffix == ".log" for path in CCD.parent.iterdir())


@pytest.mark.parametrize("kind", KINDS)
def test_generator_help_does_not_parse_or_write(tmp_path, kind):
    import molsysmt

    script = (
        Path(molsysmt.__file__).parent
        / "data"
        / "databases"
        / kind
        / f"make_{kind}_db.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "--ccd" in result.stdout and "--output-dir" in result.stdout
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("kind", KINDS)
def test_generator_import_has_no_io_side_effects(monkeypatch, tmp_path, kind):
    import molsysmt

    script = (
        Path(molsysmt.__file__).parent
        / "data"
        / "databases"
        / kind
        / f"make_{kind}_db.py"
    )
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(script))
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "kind,element_kind,code,aliases",
    [
        ("amino_acids", "amino_acid", "ALA", ["CA", "NT"]),
        ("ions", "ion", "SO4", ["O1", "S"]),
        ("saccharides", "saccharide", "GLC", ["O1", "C1"]),
        ("small_molecules", "small_molecule", "LIG", ["1O", "1C"]),
    ],
)
def test_generated_tables_deliver_bonds_through_existing_readers(
    tmp_path, monkeypatch, kind, element_kind, code, aliases
):
    from importlib import import_module

    output = tmp_path / kind
    result = _run(kind, output)
    assert result.returncode == 0, result.stderr
    package = import_module(f"molsysmt.element.group.{element_kind}")
    getter = import_module(f"molsysmt.element.group.{element_kind}.get_group_db")
    names = _load(output, "group_names.pkl.gz")
    monkeypatch.setattr(package, "group_names", names)
    monkeypatch.setattr(getter, "group_names", names)
    monkeypatch.setattr(getter, "path", lambda package, filename: output / filename)
    assert package.get_bonded_atom_pairs(code, aliases, atom_indices=[9, 4]) == [[4, 9]]


@pytest.mark.parametrize("kind", KINDS)
def test_repeated_generation_is_byte_reproducible_and_records_source(tmp_path, kind):
    outputs = [tmp_path / "first", tmp_path / "second"]
    for output in outputs:
        result = _run(kind, output)
        assert result.returncode == 0, result.stderr
    first = {path.name: path.read_bytes() for path in outputs[0].iterdir()}
    second = {path.name: path.read_bytes() for path in outputs[1].iterdir()}
    assert first == second
    manifest = json.loads(first["generation_manifest.json"])
    assert manifest["inputs"] == [
        {
            "role": "ccd",
            "filename": CCD.name,
            "sha256": hashlib.sha256(CCD.read_bytes()).hexdigest(),
        }
    ]
    assert manifest["producer"]["mmcif"] and manifest["producer"]["molsysmt"]
    assert manifest["n_groups"] == len(EXPECTED_NAMES[kind])
    for filename, digest in manifest["outputs"].items():
        assert hashlib.sha256(first[filename]).hexdigest() == digest


def test_rtp_and_supplements_are_explicit_and_preserve_variants(tmp_path):
    rtp = tmp_path / "aminoacids.rtp"
    rtp.write_text("""[ bondedtypes ]
1 1 1 1
[ ALA ]
 [ atoms ]
 N N -0.2 1
 CA C 0.2 1
 HX H 0.0 1
 [ bonds ]
 N CA
 N HX
 -C N
 CA +N
 [ impropers ]
 N CA HX -C
[ GLY ]
 [ atoms ]
 N N 0.0 1
""")
    supplement = tmp_path / "extra.json"
    supplement.write_text(
        json.dumps(
            {
                "ALA": {
                    "name": "ALANINE",
                    "topology": [
                        {
                            "atoms": ["N", "CA", "HY"],
                            "bonds": [["N", "CA"], ["N", "HY"]],
                        },
                    ],
                }
            }
        )
    )
    output = tmp_path / "amino"
    result = _run("amino_acids", output, "--rtp", str(rtp), "--extra", str(supplement))
    assert result.returncode == 0, result.stderr
    assert _load(output, "group_names.pkl.gz") == ["ALA"]
    variants = _load(output, "A.pkl.gz")["ALA"]["topology"]
    assert variants[2] == {
        "atoms": ["N", "CA", "HX"],
        "bonds": [["N", "CA"], ["N", "HX"]],
    }
    assert variants[3]["atoms"] == ["N", "CA", "HY"]
    manifest = json.loads((output / "generation_manifest.json").read_text())
    assert [item["role"] for item in manifest["inputs"]] == [
        "ccd",
        "gromacs_rtp",
        "supplemental_json",
    ]
    assert manifest["selection"]["amino_acid_names"] == ["ALA"]


def test_ion_supplement_matches_indexed_reader_schema(tmp_path):
    extra = tmp_path / "extra.json"
    extra.write_text(
        json.dumps(
            {
                "SO4": {
                    "name": "SULFATE ION",
                    "topology": [{"atoms": ["SS", "OX"], "bonds": [["SS", "OX"]]}],
                },
                "CA+2": {
                    "name": "CALCIUM ALIAS",
                    "topology": [{"atoms": ["CA+2"], "bonds": []}],
                },
            }
        )
    )
    output = tmp_path / "ions"
    result = _run("ions", output, "--extra", str(extra))
    assert result.returncode == 0, result.stderr
    assert _load(output, "C.pkl.gz")["CA+2"] == {
        "name": "CALCIUM ALIAS",
        "three_letter_code": "CA+2",
        "atom_name": [["CA+2"]],
        "bonds": [],
    }
    assert _load(output, "S.pkl.gz")["SO4"]["atom_name"][-1] == ["SS", "OX"]
    assert _load(output, "S.pkl.gz")["SO4"]["bonds"] == [[0, 1]]


@pytest.mark.parametrize("kind", KINDS)
def test_existing_caller_outputs_are_preserved(tmp_path, kind):
    output = tmp_path / "caller"
    output.mkdir()
    path = output / "A.pkl.gz"
    path.write_bytes(b"retained caller data")
    result = _run(kind, output)
    assert result.returncode != 0
    assert "Output directory must be empty" in result.stderr
    assert path.read_bytes() == b"retained caller data"
    assert sorted(p.name for p in output.iterdir()) == ["A.pkl.gz"]


@pytest.mark.parametrize(
    "defect,message",
    [
        ("bond_endpoint", "each bond must join two declared atoms"),
        ("atom_names", "atom names must be nonempty, known and unique"),
        ("alias_names", "atom names must be nonempty, known and unique"),
        ("comp_id", "inconsistent atom comp_id"),
        ("duplicate_component", "Duplicate CCD component"),
        ("empty_file", "contains no data blocks"),
        ("unsafe_name", "Unsupported group name"),
    ],
)
def test_malformed_ccd_fails_before_creating_outputs(tmp_path, defect, message):
    from molsysmt.data._make._chemical_group_database import _main

    text = CCD.read_text()
    if defect == "bond_endpoint":
        text = text.replace(
            "_chem_comp_bond.atom_id_2 O1", "_chem_comp_bond.atom_id_2 MISSING", 1
        )
    elif defect == "atom_names":
        text = text.replace("LIG O1 1O", "LIG C1 1O", 1)
    elif defect == "alias_names":
        text = text.replace("LIG O1 1O", "LIG O1 1C", 1)
    elif defect == "comp_id":
        text = text.replace("LIG O1 1O", "OTHER O1 1O", 1)
    elif defect == "duplicate_component":
        text = text.replace("_chem_comp.id ALA", "_chem_comp.id LIG", 1)
    elif defect == "empty_file":
        text = "# No components\n"
    elif defect == "unsafe_name":
        text = text.replace("_chem_comp.id LIG", "_chem_comp.id /LIG", 1)
    source = tmp_path / "invalid.cif"
    source.write_text(text)
    output = tmp_path / "output"
    with pytest.raises(ValueError, match=message):
        _main("small_molecules", ["--ccd", str(source), "--output-dir", str(output)])
    assert not output.exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["invalid.cif"]


def test_incomplete_row_after_valid_block_does_not_publish_partial_database(tmp_path):
    from molsysmt.data._make._chemical_group_database import _main

    source = tmp_path / "broken.cif"
    source.write_text(
        CCD.read_text() + "data_BROKEN\nloop_\n_chem_comp.id\n_chem_comp.name\nBROKEN\n"
    )
    output = tmp_path / "output"
    with pytest.raises(ValueError, match="incomplete chem_comp row"):
        _main("ions", ["--ccd", str(source), "--output-dir", str(output)])
    assert not output.exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["broken.cif"]


def test_existing_ion_supplements_generate_reader_schema(tmp_path):
    import molsysmt
    from molsysmt.data._make._chemical_group_database import _main

    database_root = Path(molsysmt.__file__).parent / "data" / "databases"
    extra = database_root / "ions" / "extra.json"
    output = tmp_path / "ions"
    _main(
        "ions",
        ["--ccd", str(CCD), "--output-dir", str(output), "--extra", str(extra)],
    )
    assert set(json.loads(extra.read_text())) <= set(
        _load(output, "group_names.pkl.gz")
    )
    for prefix in {code[0] for code in _load(output, "group_names.pkl.gz")}:
        for record in _load(output, prefix + ".pkl.gz").values():
            assert "atom_name" in record and "bonds" in record
            assert "topology" not in record


def test_invalid_amino_acid_supplement_is_rejected_before_writing(tmp_path):
    from molsysmt.data._make._chemical_group_database import _main

    # Equivalent to the undeclared OXT endpoint in the legacy MET supplement (#380).
    extra = tmp_path / "invalid.json"
    extra.write_text(
        json.dumps(
            {"MET": {"topology": [{"atoms": ["C", "O"], "bonds": [["C", "OXT"]]}]}}
        )
    )
    output = tmp_path / "output"
    with pytest.raises(
        ValueError, match="Group MET: each bond must join two declared atoms"
    ):
        _main(
            "amino_acids",
            ["--ccd", str(CCD), "--output-dir", str(output), "--extra", str(extra)],
        )
    assert not output.exists()


def test_compressed_ccd_produces_same_reference_tables(tmp_path):
    from molsysmt.data._make._chemical_group_database import _main

    source = tmp_path / "components.cif.gz"
    with gzip.open(source, "wb") as stream:
        stream.write(CCD.read_bytes())
    output = tmp_path / "compressed"
    plain = tmp_path / "plain"
    for path, destination in [(source, output), (CCD, plain)]:
        _main("ions", ["--ccd", str(path), "--output-dir", str(destination)])
    for filename in ["N.pkl.gz", "S.pkl.gz", "group_names.pkl.gz"]:
        assert (output / filename).read_bytes() == (plain / filename).read_bytes()
    assert (
        json.loads((output / "generation_manifest.json").read_text())["inputs"][0][
            "sha256"
        ]
        == hashlib.sha256(source.read_bytes()).hexdigest()
    )


def test_curated_real_ccd_retains_mse_connectivity(tmp_path):
    import molsysmt
    from molsysmt.data._make._chemical_group_database import _main

    source = (
        Path(molsysmt.__file__).parent / "data" / "_make" / "ccd_components" / "MSE.cif"
    )
    output = tmp_path / "mse"
    _main(
        "amino_acids",
        [
            "--ccd",
            str(source),
            "--output-dir",
            str(output),
            "--amino-acid-name",
            "MSE",
        ],
    )
    topology = _load(output, "M.pkl.gz")["MSE"]["topology"][0]
    assert "SE" in topology["atoms"]
    bonds = {frozenset(pair) for pair in topology["bonds"]}
    assert {frozenset(["CG", "SE"]), frozenset(["SE", "CE"])} <= bonds


def test_empty_selected_family_has_valid_empty_index(tmp_path):
    from molsysmt.data._make._chemical_group_database import _main

    source = tmp_path / "sodium.cif"
    block = CCD.read_text().split("data_NA\n")[1].split("data_ALA\n")[0]
    source.write_text("data_NA\n" + block)
    output = tmp_path / "no_sugars"
    _main("saccharides", ["--ccd", str(source), "--output-dir", str(output)])
    assert _load(output, "group_names.pkl.gz") == []
    assert sorted(p.name for p in output.iterdir()) == [
        "generation_manifest.json",
        "group_names.pkl.gz",
    ]
