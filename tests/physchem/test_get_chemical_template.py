"""Checking explicit CCD acquisition and coordinate-free reference identity."""

import base64
import gzip
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.ccd_reference import read_definition
from molsysmt._private.smonitor import (
    ChemicalReferenceLookupError,
    FileContentError,
    UnsupportedHeavyOperationError,
)


def component_definition(component_id="ONE", *, block_name=None):
    return (
        f"data_{component_id if block_name is None else block_name}\n"
        f"_chem_comp.id {component_id}\n"
        "_chem_comp.pdbx_modified_date 2026-01-02\n"
        "loop_\n_chem_comp_atom.comp_id\n_chem_comp_atom.atom_id\n"
        "_chem_comp_atom.type_symbol\n_chem_comp_atom.charge\n"
        f"{component_id} C1 C 0\n#\n"
    ).encode()


@pytest.mark.parametrize("storage", ["bytes", "file", "gzip", "directory"])
def test_explicit_sources_retain_the_original_definition_and_resource_digest(
    tmp_path, storage
):
    definition = b"# caller preamble\r\n" + component_definition().replace(
        b"\n", b"\r\n"
    )
    raw = gzip.compress(definition, mtime=0) if storage == "gzip" else definition
    source = raw
    if storage != "bytes":
        path = tmp_path / ("ONE.cif.gz" if storage == "gzip" else "ONE.cif")
        path.write_bytes(raw)
        source = tmp_path if storage == "directory" else path
    block, record = read_definition("ONE", source)
    assert block.getObj("chem_comp_atom").getValue("atom_id", 0) == "C1"
    assert record["component_id"] == "ONE"
    assert record["version"] == "2026-01-02"
    assert record["resource_sha256"] == sha256(raw).hexdigest()
    assert record["resource_n_bytes"] == len(raw)
    assert record["definition_sha256"] == sha256(definition).hexdigest()
    assert base64.b64decode(record["definition"]["data"]) == definition
    assert record["definition_decompressed_offset"] == 0


def test_catalogue_lookup_respects_multiline_values_and_exact_block_bytes(tmp_path):
    first = component_definition("OTHER") + b"_chem_comp.name\n;\ndata_ONE\n;\n"
    selected = component_definition()
    last = component_definition("LAST")
    raw = first + selected + last
    path = tmp_path / "catalogue.cif"
    path.write_bytes(raw)
    block, record = read_definition("ONE", path)
    assert block.getObj("chem_comp").getValue("id", 0) == "ONE"
    assert base64.b64decode(record["definition"]["data"]) == selected
    assert record["definition_decompressed_offset"] == len(first)
    assert record["resource_sha256"] == sha256(raw).hexdigest()


def test_one_component_file_can_declare_its_id_under_a_different_block_label():
    block, record = read_definition("ONE", component_definition(block_name="reference"))
    assert record["block_name"] == "reference"
    assert block.getObj("chem_comp").getValue("id", 0) == "ONE"


def test_duplicate_component_blocks_are_not_resolved_by_first_match():
    raw = component_definition() + component_definition()
    with pytest.raises(ChemicalReferenceLookupError) as caught:
        read_definition("ONE", raw)
    assert caught.value.reason == "ambiguous"


@pytest.mark.parametrize("declaration", [b"?", b".", b"''"])
def test_missing_component_identity_is_invalid_content_not_an_offline_miss(declaration):
    raw = component_definition().replace(
        b"_chem_comp.id ONE", b"_chem_comp.id " + declaration
    )
    with pytest.raises(FileContentError, match="chem_comp.id"):
        read_definition("ONE", raw)


@pytest.mark.parametrize("storage", ["directory", "catalogue", "missing_file"])
def test_offline_misses_never_attempt_network_fallback(tmp_path, monkeypatch, storage):
    from molsysmt._private import download

    def forbidden(*args, **kwargs):
        pytest.fail("An offline chemical-reference miss must remain offline")

    monkeypatch.setattr(download, "download_with_retries", forbidden)
    source = tmp_path
    if storage != "directory":
        source = tmp_path / "catalogue.cif"
        if storage == "catalogue":
            source.write_bytes(component_definition("OTHER"))
    with pytest.raises(ChemicalReferenceLookupError) as caught:
        read_definition("ONE", source)
    assert caught.value.reason == "not_found"
    if storage == "missing_file":
        assert isinstance(caught.value.__cause__, FileNotFoundError)


def test_multiple_local_candidates_require_an_explicit_choice(tmp_path):
    (tmp_path / "ONE.cif").write_bytes(component_definition())
    (tmp_path / "one.cif.gz").write_bytes(
        gzip.compress(component_definition(), mtime=0)
    )
    with pytest.raises(ChemicalReferenceLookupError) as caught:
        read_definition("ONE", tmp_path)
    assert caught.value.reason == "ambiguous"


def test_explicit_online_route_uses_the_existing_single_component_downloader(
    monkeypatch,
):
    from molsysmt._private import download

    calls = []

    def supplied(url, output_filename, resource, provider, caller):
        calls.append((url, output_filename))
        Path(output_filename).write_bytes(component_definition())

    monkeypatch.setattr(download, "download_with_retries", supplied)
    block, record = read_definition("ONE", "rcsb")
    assert block.getObj("chem_comp").getValue("id", 0) == "ONE"
    assert record["kind"] == "rcsb"
    assert calls[0][0] == "https://files.rcsb.org/ligands/download/ONE.cif"
    assert not Path(calls[0][1]).exists()


@pytest.mark.parametrize("http_status", [404, 503])
def test_online_lookup_keeps_not_found_distinct_from_unavailable_and_retains_cause(
    monkeypatch, http_status
):
    from molsysmt._private import download

    def unavailable(*args, **kwargs):
        try:
            raise HTTPError(
                "https://example.invalid", http_status, "controlled", {}, None
            )
        except HTTPError as error:
            raise RuntimeError("controlled acquisition failure") from error

    monkeypatch.setattr(download, "download_with_retries", unavailable)
    with pytest.raises(ChemicalReferenceLookupError) as caught:
        read_definition("ONE", "rcsb")
    assert caught.value.reason == ("not_found" if http_status == 404 else "unavailable")
    assert isinstance(caught.value.__cause__, RuntimeError)
    assert caught.value.__cause__.__cause__.code == http_status


def test_truncated_gzip_is_invalid_content_rather_than_a_missing_reference():
    raw = gzip.compress(component_definition(), mtime=0)[:-6]
    with pytest.raises(FileContentError, match="compressed CCD"):
        read_definition("ONE", raw)


def test_source_replacement_during_read_rejects_the_result(tmp_path, monkeypatch):
    from molsysmt._private import ccd_reference

    path = tmp_path / "ONE.cif"
    path.write_bytes(component_definition())
    select = ccd_reference._select_block

    def replacing(*args):
        result = select(*args)
        replacement = tmp_path / "replacement.cif"
        replacement.write_bytes(component_definition())
        replacement.replace(path)
        return result

    monkeypatch.setattr(ccd_reference, "_select_block", replacing)
    with pytest.raises(ChemicalReferenceLookupError) as caught:
        read_definition("ONE", path)
    assert caught.value.reason == "source_changed"


def test_large_catalogue_lookup_uses_bounded_raw_reads(tmp_path, monkeypatch):
    import tracemalloc

    from molsysmt._private import ccd_reference

    path = tmp_path / "catalogue.cif"
    with path.open("wb") as stream:
        for index in range(10000):
            stream.write(component_definition("REF" + str(index)))
        stream.write(component_definition())
    requested = []
    original = ccd_reference._DigestReader.readinto

    def bounded(self, buffer):
        requested.append(len(buffer))
        assert len(buffer) <= 65536
        return original(self, buffer)

    monkeypatch.setattr(ccd_reference._DigestReader, "readinto", bounded)
    read_definition("ONE", component_definition())
    requested.clear()
    tracemalloc.start()
    try:
        block, record = read_definition("ONE", path)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert peak < path.stat().st_size // 2
    assert requested and len(requested) > 10
    assert record["resource_n_bytes"] == path.stat().st_size
    assert record["definition_n_bytes"] == len(component_definition())
    assert block.getObj("chem_comp_atom").getRowCount() == 1


REFERENCE_INPUTS = Path(__file__).parent / "data" / "chemical_templates"


@pytest.mark.parametrize(
    "component_id,heavy,hydrogens", [("MK1", 45, 47), ("BTN", 16, 16)]
)
@pytest.mark.parametrize("hydrogen_policy", ["stored_counts", "explicit_atoms"])
def test_general_constructor_retains_full_source_identity_and_hydrogen_inventory(
    component_id, heavy, hydrogens, hydrogen_policy
):
    raw = (REFERENCE_INPUTS / (component_id + ".cif")).read_bytes()
    result = msm.physchem.get_chemical_template(
        component_id.lower(), raw, hydrogen_policy=hydrogen_policy
    )
    report, template = result["report"], result["template"]
    assert report["status"] == "constructed"
    assert template.structures is None
    assert report["n_source_atoms"] == heavy + hydrogens
    assert template.get(n_atoms=True) == (
        heavy if hydrogen_policy == "stored_counts" else heavy + hydrogens
    )
    assert report["n_stored_hydrogens"] == (
        hydrogens if hydrogen_policy == "stored_counts" else 0
    )
    assert report["n_indexed_hydrogens"] == (
        0 if hydrogen_policy == "stored_counts" else hydrogens
    )
    mapping = report["atom_map"]
    keep = mapping["output_to_source_atom_indices"]
    inverse = mapping["source_to_output_atom_indices"]
    np.testing.assert_array_equal(inverse[keep], np.arange(len(keep)))
    assert keep.dtype == inverse.dtype == np.int64
    assert template.topology.atoms["atom_name"].tolist() == [
        report["source_atom_ids"][i] for i in keep
    ]
    assert all(isinstance(label, str) for label in template.topology.atoms["atom_id"])
    assert report["source"]["resource_sha256"] == sha256(raw).hexdigest()
    assert raw == (REFERENCE_INPUTS / (component_id + ".cif")).read_bytes()
    assert report["descriptor"]["search_complete"]
    assert report["descriptor"]["assignment_consensus_complete"]


def test_symmetric_descriptor_maps_must_reach_a_complete_assignment_consensus():
    source = REFERENCE_INPUTS / "MK1.cif"
    result = msm.physchem.get_chemical_template("MK1", source)
    descriptor = result["report"]["descriptor"]
    assert descriptor["n_graph_matches"] == descriptor["n_compatible_matches"] == 12
    assert descriptor["assignment_consensus_complete"]
    with pytest.raises(UnsupportedHeavyOperationError, match="max_matches"):
        msm.physchem.get_chemical_template("MK1", source, max_matches=1)


def test_est_stereo_disagreement_is_retained_under_the_explicit_descriptor_policy():
    result = msm.physchem.get_chemical_template("EST", REFERENCE_INPUTS / "EST.cif")
    assert result["report"]["status"] == "constructed"
    disagreements = result["report"]["descriptor"]["stereo_disagreements"]
    assert disagreements == [
        dict(
            axis="atom",
            source_index=8,
            source_atom_id="C8",
            ccd_flag="S",
            chosen_descriptor_label="R",
        )
    ]
    atoms = result["template"].topology.atoms
    labels = (
        result["template"].chemical_states._states[0].atom_attributes["stereochemistry"]
    )
    expected = {"C8": "R", "C9": "S", "C13": "S", "C14": "S", "C17": "S"}
    for name, label in expected.items():
        assert labels.iloc[atoms.index[atoms["atom_name"].eq(name)][0]] == label


def test_table_projection_keeps_unsupported_chemistry_unknown():
    raw = component_definition().replace(b"C1 C 0", b"C1 C ?")
    result = msm.physchem.get_chemical_template("ONE", raw, method="ccd_tables")
    assert result["report"]["status"] == "unassessed"
    state = result["template"].chemical_states._states[0]
    assert state.atom_attributes["formal_charge"].isna().all()
    assert state.atom_attributes["n_unpaired_electrons"].isna().all()
    assert "rdkit" not in result["report"]["software"]


def _hydroxide_definition(hydrogen_charge="0"):
    return (
        "data_ION\n_chem_comp.id ION\n"
        "loop_\n_chem_comp_atom.comp_id\n_chem_comp_atom.atom_id\n"
        "_chem_comp_atom.type_symbol\n_chem_comp_atom.charge\n"
        "_chem_comp_atom.pdbx_aromatic_flag\n_chem_comp_atom.pdbx_stereo_config\n"
        f"ION O1 O -1 N N\nION H1 H {hydrogen_charge} N N\n#\n"
        "loop_\n_chem_comp_bond.comp_id\n_chem_comp_bond.atom_id_1\n"
        "_chem_comp_bond.atom_id_2\n_chem_comp_bond.value_order\n"
        "_chem_comp_bond.pdbx_aromatic_flag\n_chem_comp_bond.pdbx_stereo_config\n"
        "ION O1 H1 SING N N\n#\n"
    ).encode()


def test_stored_h_projection_cannot_discard_an_unknown_hydrogen_charge():
    from molsysmt._private.smonitor import StructuralInconsistencyError

    raw = _hydroxide_definition("?")
    explicit = msm.physchem.get_chemical_template(
        "ION", raw, method="ccd_tables", hydrogen_policy="explicit_atoms"
    )
    assert explicit["template"].chemical_states._states[0].atom_attributes[
        "formal_charge"
    ].isna().tolist() == [False, True]
    with pytest.raises(StructuralInconsistencyError, match="without loss"):
        msm.physchem.get_chemical_template(
            "ION", raw, method="ccd_tables", hydrogen_policy="stored_counts"
        )


def test_reference_charge_has_explicit_units_under_a_nondefault_policy():
    raw = _hydroxide_definition()
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        result = msm.physchem.get_chemical_template("ION", raw, method="ccd_tables")
        template = result["template"]
        charges = msm.get(template, element="atom", formal_charge=True)
        # Formal charges are stored integer multiples of e, independently of
        # the session's unit for continuously valued electric charge.
        np.testing.assert_array_equal(charges, [-1])
        assert result["report"]["units"]["formal_charge"] == "elementary_charge"
        assert result["report"]["n_stored_hydrogens"] == 1
        assert template.structures is None


def test_atom_and_bond_row_permutations_keep_identity_instead_of_positional_assumptions():
    import io

    from mmcif.io.PdbxReader import PdbxReader
    from mmcif.io.PdbxWriter import PdbxWriter

    raw = (REFERENCE_INPUTS / "BTN.cif").read_bytes()
    original = msm.physchem.get_chemical_template("BTN", raw)
    blocks = []
    PdbxReader(io.StringIO(raw.decode())).read(blocks)
    for category in ("chem_comp_atom", "chem_comp_bond"):
        table = blocks[0].getObj(category)
        rows = [list(table.getRow(i)) for i in range(table.getRowCount())]
        table.setRowList(list(reversed(rows)))
    output = io.StringIO()
    PdbxWriter(output).write(blocks)
    permuted = msm.physchem.get_chemical_template("BTN", output.getvalue().encode())
    for result in (original, permuted):
        names = result["template"].topology.atoms["atom_name"].tolist()
        keep = result["report"]["atom_map"]["output_to_source_atom_indices"]
        assert names == [result["report"]["source_atom_ids"][i] for i in keep]
    first = original["template"].topology.atoms["atom_name"].tolist()
    second = permuted["template"].topology.atoms["atom_name"].tolist()
    assert first == second[::-1]
    for field in (
        "formal_charge",
        "is_aromatic",
        "n_unpaired_electrons",
        "n_explicit_hydrogens",
        "stereochemistry",
    ):
        a = (
            original["template"]
            .chemical_states._states[0]
            .atom_attributes[field]
            .tolist()
        )
        b = (
            permuted["template"]
            .chemical_states._states[0]
            .atom_attributes[field]
            .tolist()
        )
        assert dict(zip(first, a)) == dict(zip(second, b))


def test_source_provenance_history_and_values_roundtrip_without_coordinate_domain(
    tmp_path,
):
    import json

    import pandas as pd

    result = msm.physchem.get_chemical_template("BTN", REFERENCE_INPUTS / "BTN.cif")
    json.dumps(result["template_provenance"], allow_nan=False)
    path = tmp_path / "reference.h5msm"
    msm.h5msm.write(result["template"], path)
    restored = msm.h5msm.read(path)
    assert restored.structures is None
    pd.testing.assert_frame_equal(
        restored.chemical_states._states[0].atom_attributes,
        result["template"].chemical_states._states[0].atom_attributes,
    )
    history = restored.chemical_states.get_preparation_history()[0]["report"]
    assert history["software"] == result["report"]["software"]
    assert history["source"]["definition"] == result["report"]["source"]["definition"]
    np.testing.assert_array_equal(
        history["atom_map"]["output_to_source_atom_indices"],
        result["report"]["atom_map"]["output_to_source_atom_indices"],
    )


@pytest.mark.parametrize("component_id", [None, True, 1, "", "../ONE", "O NE", ["ONE"]])
def test_invalid_reference_identifiers_fail_at_the_public_boundary(component_id):
    with pytest.raises(msm.ArgumentError):
        msm.physchem.get_chemical_template(
            component_id, component_definition(), method="ccd_tables"
        )


def test_lookup_diagnostic_roundtrips_with_its_structured_identity():
    import pickle

    original = ChemicalReferenceLookupError(
        "ONE", "caller:bytes", "not_found", caller="fixture.lookup"
    )
    restored = pickle.loads(pickle.dumps(original))
    assert restored.component_id == "ONE"
    assert restored.resource == "caller:bytes"
    assert restored.reason == "not_found"
    assert str(restored) == str(original)
