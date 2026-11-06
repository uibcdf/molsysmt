"""Qualifying declared CCD chemistry and descriptor ambiguity, not conformers."""

import io
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from mmcif.api.DataCategory import DataCategory
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter

import molsysmt as msm
from molsysmt._private.smonitor import FileContentError, MemoryBudgetExceededError

DATA = Path(__file__).parent / "data" / "chemical_templates"


def _bytes(block):
    output = io.StringIO()
    PdbxWriter(output).write([block])
    return output.getvalue().encode()


def _parse(raw):
    blocks = []
    PdbxReader(io.StringIO(raw.decode())).read(blocks)
    return blocks[0]


def _reference(smiles):
    """Build a labelled test declaration; its literal SMILES is the criterion."""
    Chem = pytest.importorskip("rdkit.Chem")
    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    Chem.Kekulize(molecule, clearAromaticFlags=False)
    names = [atom.GetSymbol() + str(atom.GetIdx()) for atom in molecule.GetAtoms()]
    text = "data_TST\n_chem_comp.id TST\n_chem_comp.pdbx_modified_date 2026-01-01\n"
    block = _parse(text.encode())
    block.append(
        DataCategory(
            "chem_comp_atom",
            attributeNameList=[
                "comp_id",
                "atom_id",
                "type_symbol",
                "charge",
                "pdbx_aromatic_flag",
                "pdbx_stereo_config",
            ],
            rowList=[
                [
                    "TST",
                    names[a.GetIdx()],
                    a.GetSymbol(),
                    str(a.GetFormalCharge()),
                    "Y" if a.GetIsAromatic() else "N",
                    "N",
                ]
                for a in molecule.GetAtoms()
            ],
        )
    )
    orders = {
        Chem.BondType.SINGLE: "SING",
        Chem.BondType.DOUBLE: "DOUB",
        Chem.BondType.TRIPLE: "TRIP",
    }
    if molecule.GetNumBonds():
        block.append(
            DataCategory(
                "chem_comp_bond",
                attributeNameList=[
                    "comp_id",
                    "atom_id_1",
                    "atom_id_2",
                    "value_order",
                    "pdbx_aromatic_flag",
                    "pdbx_stereo_config",
                ],
                rowList=[
                    [
                        "TST",
                        names[b.GetBeginAtomIdx()],
                        names[b.GetEndAtomIdx()],
                        orders[b.GetBondType()],
                        "Y" if b.GetIsAromatic() else "N",
                        "N",
                    ]
                    for b in molecule.GetBonds()
                ],
            )
        )
    block.append(
        DataCategory(
            "pdbx_chem_comp_descriptor",
            attributeNameList=[
                "comp_id",
                "type",
                "program",
                "program_version",
                "descriptor",
            ],
            rowList=[["TST", "SMILES_CANONICAL", "fixture", "1", smiles]],
        )
    )
    return block


def _construct(block, **kwargs):
    return msm.physchem.get_chemical_template(
        "TST", _bytes(block), descriptor_program="fixture", **kwargs
    )


@pytest.mark.parametrize(
    "smiles,charges,hydrogens,radicals",
    [
        ("[NH4+]", [1], [4], [0]),
        ("[O-]C=O", [-1, 0, 0], [0, 1, 0], [0, 0, 0]),
        ("[CH3]", [0], [3], [1]),
    ],
)
def test_charged_and_radical_references_retain_declared_counts(
    smiles, charges, hydrogens, radicals
):
    result = _construct(_reference(smiles))
    assert result["report"]["status"] == "constructed"
    attributes = result["template"].chemical_states._states[0].atom_attributes
    assert attributes.formal_charge.tolist() == charges
    assert attributes.n_explicit_hydrogens.tolist() == hydrogens
    assert attributes.n_unpaired_electrons.tolist() == radicals
    assert result["report"]["units"]["formal_charge"] == "elementary_charge"


@pytest.mark.parametrize("smiles,label", [("F/C=C/F", "E"), ("F/C=C\\F", "Z")])
def test_double_bond_stereo_and_endpoint_reference_atoms_survive_row_permutation(
    smiles, label
):
    block = _reference(smiles)
    for category in ("chem_comp_atom", "chem_comp_bond"):
        table = block.getObj(category)
        table.setRowList(list(reversed([list(row) for row in table.getRowList()])))
    result = _construct(block)
    assert result["report"]["status"] == "constructed"
    topology = result["template"].topology
    bonds = result["template"].chemical_states.get_bonds()
    stereo = bonds[bonds.stereochemistry.notna()]
    assert len(stereo) == 1
    row = stereo.iloc[0]
    assert row.stereochemistry == label
    names = topology.atoms.atom_name
    assert {
        names.iloc[int(row.stereo_atom1_index)],
        names.iloc[int(row.stereo_atom2_index)],
    } == {"F0", "F3"}
    pairs = {
        tuple(sorted((int(b.atom1_index), int(b.atom2_index))))
        for b in bonds.itertuples()
    }
    for endpoint, reference in (
        (row.atom1_index, row.stereo_atom1_index),
        (row.atom2_index, row.stereo_atom2_index),
    ):
        assert tuple(sorted((int(endpoint), int(reference)))) in pairs


def test_unspecified_stereogenic_descriptor_is_not_a_complete_stereo_assignment():
    result = _construct(_reference("FC(Cl)(Br)I"))
    assert result["report"]["status"] == "unassessed"
    assert "unassigned_descriptor_stereochemistry" in {
        i["reason"] for i in result["report"]["issues"]
    }
    assert (
        result["template"]
        .chemical_states._states[0]
        .atom_attributes.stereochemistry.isna()
        .all()
    )


@pytest.mark.parametrize(
    "smiles,status",
    [("C[C@H](F)[C@H](F)C", "conflict"), ("C[C@H](F)[C@@H](F)C", "constructed")],
)
def test_symmetric_stereo_transfer_requires_agreement_across_all_maps(smiles, status):
    result = _construct(_reference(smiles))
    report = result["report"]
    assert report["status"] == status
    assert report["descriptor"]["n_graph_matches"] == 2
    assert report["descriptor"]["n_compatible_matches"] == 2
    if status == "conflict":
        assert "descriptor_assignment_ambiguous" in {
            i["reason"] for i in report["issues"]
        }
        assert not report["descriptor"]["assignment_consensus_complete"]
        assert (
            result["template"]
            .chemical_states._states[0]
            .atom_attributes.stereochemistry.isna()
            .all()
        )
    else:
        assert report["descriptor"]["assignment_consensus_complete"]


def test_a_descriptor_declared_for_another_component_is_not_transferred():
    block = _reference("CO")
    block.getObj("pdbx_chem_comp_descriptor").setValue("OTHER", "comp_id", 0)
    with pytest.raises(FileContentError, match="descriptor.*component"):
        _construct(block)


@pytest.mark.parametrize(
    "damage",
    ["missing", "duplicate", "different_program", "invalid_smiles", "wrong_charge"],
)
def test_missing_ambiguous_and_conflicting_descriptors_remain_explicit(damage):
    block = _reference("[NH4+]")
    table = block.getObj("pdbx_chem_comp_descriptor")
    if damage == "missing":
        table.setValue("SMILES", "type", 0)
    elif damage == "duplicate":
        table.append(list(table.getRow(0)))
    elif damage == "different_program":
        table.setValue("other", "program", 0)
    elif damage == "invalid_smiles":
        table.setValue("[broken", "descriptor", 0)
    else:
        table.setValue("N", "descriptor", 0)
    result = _construct(block)
    reasons = {i["reason"] for i in result["report"]["issues"]}
    assert result["report"]["status"] in {"unassessed", "conflict"}
    assert reasons.intersection(
        {
            "canonical_descriptor_not_found",
            "canonical_descriptor_ambiguous",
            "invalid_canonical_descriptor",
            "descriptor_chemistry_conflict",
        }
    )
    assert not result["report"]["descriptor"]["assignment_consensus_complete"]


@pytest.mark.parametrize(
    "damage", ["duplicate_atom", "missing_name", "dangling_bond", "duplicate_bond"]
)
def test_malformed_reference_axes_are_not_silently_repaired(damage):
    block = _reference("CO")
    atoms, bonds = block.getObj("chem_comp_atom"), block.getObj("chem_comp_bond")
    if damage == "duplicate_atom":
        atoms.setValue(atoms.getValue("atom_id", 0), "atom_id", 1)
    elif damage == "missing_name":
        atoms.setValue("?", "atom_id", 0)
    elif damage == "dangling_bond":
        bonds.setValue("absent", "atom_id_1", 0)
    else:
        bonds.append(list(bonds.getRow(0)))
    with pytest.raises(FileContentError):
        _construct(block)


def test_descriptor_search_respects_the_configured_candidate_memory_budget():
    from molsysmt._private.ccd_descriptor import interpret
    from molsysmt._private.chemical_reference_template import _tables

    block = _reference("c1ccccc1")
    atoms, bonds, _ = _tables(block, "TST", [])
    with msm.configure.context(max_ram_usage=100):
        with pytest.raises(MemoryBudgetExceededError, match="correspondence"):
            interpret(block, atoms, bonds, "fixture", 4096)


@pytest.mark.parametrize("region", ["physical_line", "preamble", "selected_block"])
def test_reference_input_buffers_fail_explicitly_under_the_memory_budget(region):
    from molsysmt._private.ccd_reference import read_definition

    definition = _bytes(_reference("O"))
    comments = b"#" + b"x" * 128 + b"\n"
    if region == "physical_line":
        resource = b"#" + b"x" * 100000 + b"\n" + definition
    elif region == "preamble":
        resource = comments * 500 + definition
    else:
        resource = definition + comments * 500
    with msm.configure.context(max_ram_usage=100000):
        with pytest.raises(MemoryBudgetExceededError, match="input buffer budget"):
            read_definition("TST", resource)


@pytest.mark.parametrize(
    "damage", ["aromatic_triple", "aromatic_quadruple", "nonaromatic_endpoint"]
)
def test_contradictory_aromatic_declarations_cannot_certify_a_descriptor(damage):
    block = _reference("c1ccccc1")
    bonds = block.getObj("chem_comp_bond")
    if damage == "nonaromatic_endpoint":
        block.getObj("chem_comp_atom").setValue("N", "pdbx_aromatic_flag", 0)
    else:
        bonds.setValue(
            "TRIP" if damage == "aromatic_triple" else "QUAD", "value_order", 0
        )
    result = _construct(block)
    reason = (
        "contradictory_aromatic_declarations"
        if damage == "nonaromatic_endpoint"
        else "unsupported_aromatic_bond_order"
    )
    assert result["report"]["status"] == (
        "conflict" if damage == "nonaromatic_endpoint" else "unassessed"
    )
    assert reason in {i["reason"] for i in result["report"]["issues"]}
    assert not result["report"]["descriptor"]["assignment_consensus_complete"]


@pytest.mark.parametrize("method", ["ccd_tables", "ccd_canonical_descriptor"])
def test_ccd_case_insensitive_codes_keep_the_same_declared_chemistry(method):
    raw = (DATA / "BTN.cif").read_bytes()
    block = _parse(raw)
    for category in ("chem_comp_atom", "chem_comp_bond"):
        table = block.getObj(category)
        for field in ("pdbx_aromatic_flag", "pdbx_stereo_config", "value_order"):
            if table.hasAttribute(field):
                for row in range(table.getRowCount()):
                    table.setValue(table.getValue(field, row).lower(), field, row)
    expected = msm.physchem.get_chemical_template("BTN", raw, method=method)
    actual = msm.physchem.get_chemical_template("BTN", _bytes(block), method=method)
    assert actual["report"]["status"] == expected["report"]["status"]
    assert (
        actual["template"]
        .chemical_states._states[0]
        .atom_attributes.equals(
            expected["template"].chemical_states._states[0].atom_attributes
        )
    )
    assert (
        actual["template"]
        .chemical_states.get_bonds()
        .equals(expected["template"].chemical_states.get_bonds())
    )


def test_component_and_atom_charge_disagreement_is_retained_as_a_conflict():
    block = _reference("[NH4+]")
    block.getObj("chem_comp").appendAttribute("pdbx_formal_charge")
    block.getObj("chem_comp").setValue("0", "pdbx_formal_charge", 0)
    result = _construct(block)
    assert result["report"]["status"] == "conflict"
    assert result["report"]["component_formal_charge"] == {
        "declared": 0,
        "atom_sum": 1,
        "unit": "elementary_charge",
    }
    assert result["template"].chemical_states._states[
        0
    ].atom_attributes.formal_charge.tolist() == [1]
    assert "component_formal_charge_conflict" in {
        i["reason"] for i in result["report"]["issues"]
    }
    assert not result["report"]["descriptor"]["assignment_consensus_complete"]


@pytest.mark.parametrize("method", ["ccd_tables", "ccd_canonical_descriptor"])
def test_unrepresentable_charge_is_refused_at_the_reference_boundary(method):
    block = _reference("[NH4+]")
    block.getObj("chem_comp_atom").setValue("100000000000000000000", "charge", 0)
    with pytest.raises(FileContentError, match="formal.charge"):
        _construct(block, method=method)


@pytest.mark.parametrize("damage", ["isotope", "charged", "isolated", "multiple_links"])
def test_lossy_hydrogen_projection_refuses_but_explicit_tables_preserve_the_axis(
    damage,
):
    block = _reference("O")
    atoms, bonds = block.getObj("chem_comp_atom"), block.getObj("chem_comp_bond")
    if damage == "isotope":
        atoms.setValue("D", "type_symbol", 1)
    elif damage == "charged":
        atoms.setValue("1", "charge", 1)
    elif damage == "isolated":
        bonds.removeRow(0)
    else:
        bonds.append(["TST", "H1", "H2", "SING", "N", "N"])
    with pytest.raises(msm.StructuralInconsistencyError):
        _construct(block, method="ccd_tables")
    result = _construct(block, method="ccd_tables", hydrogen_policy="explicit_atoms")
    assert result["report"]["n_source_atoms"] == result["report"]["n_atoms"] == 3
    np.testing.assert_array_equal(
        result["report"]["atom_map"]["source_to_output_atom_indices"], [0, 1, 2]
    )
    if damage == "isotope":
        assert result["template"].topology.atoms.isotope.iloc[1] == 2
    if damage == "charged":
        assert (
            result["template"]
            .chemical_states._states[0]
            .atom_attributes.formal_charge.iloc[1]
            == 1
        )


def test_native_tables_work_in_a_fresh_process_without_optional_engines_or_ackredit():
    script = """
import importlib.abc, sys
original_finders = tuple(sys.meta_path)
class Absent(importlib.abc.MetaPathFinder):
    def find_distributions(self, context=None):
        for finder in original_finders:
            method = getattr(finder,'find_distributions',None)
            if method is not None:
                yield from method(context=context)
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit','ackredit','meeko'}:
            return None
        for finder in original_finders:
            method = getattr(finder,'find_spec',None)
            result = method(fullname,path,target) if method is not None else None
            if result is not None:
                return result
        return None
sys.meta_path[:] = [Absent()]
import molsysmt as msm
assert 'ackredit' not in sys.modules and 'rdkit' not in sys.modules
result = msm.physchem.get_chemical_template('BTN',sys.argv[1],method='ccd_tables')
assert result['report']['status'] == 'unassessed'
assert result['template'].structures is None
assert not any(name in sys.modules for name in ('rdkit','ackredit','meeko'))
assert result['report']['attribution']['items']
try:
    msm.physchem.get_chemical_template('BTN',sys.argv[1])
except msm.LibraryNotFoundError:
    pass
else:
    raise AssertionError('Canonical method must refuse the absent selected engine')
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(DATA / "BTN.cif")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_real_ackredit_reused_data_and_criterion_remain_detached_in_every_result(
    tmp_path,
):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("CCD consumer"):
        with ackredit.capture("references") as capture:
            first = msm.physchem.get_chemical_template("BTN", DATA / "BTN.cif")
            second = msm.physchem.get_chemical_template("BTN", DATA / "BTN.cif")
        ids = {item["id"] for item in first["report"]["attribution"]["items"]}
        assert ids == {item["id"] for item in second["report"]["attribution"]["items"]}
        assert "doi:10.1021/acs.jcim.8b00324" in ids
        assert "doi:10.1093/bioinformatics/btu789" in ids
        assert ids.issubset(set(ackredit.get_used_items()))
        portable = capture.attribution.to_dict()
        assert ackredit.Attribution.from_dict(portable).to_dict() == portable
        assert not any(item.startswith("software:CACTVS") for item in ids)
    article = next(
        i
        for i in first["report"]["attribution"]["items"]
        if i["id"] == "doi:10.1093/bioinformatics/btu789"
    )
    article["authors"][0] = "changed"
    original = next(
        i for i in second["report"]["attribution"]["items"] if i["id"] == article["id"]
    )
    assert original["authors"][0] != "changed"
    original_bytes = first["template_provenance"]["source"]["definition"]["data"]
    first["report"]["source"]["definition"]["data"] = "changed"
    assert (
        first["template_provenance"]["source"]["definition"]["data"] == original_bytes
    )
    path = tmp_path / "reference.h5msm"
    msm.convert(second["template"], to_form=path)
    with ackredit.session("read saved reference"):
        restored = msm.convert(path, to_form="molsysmt.MolSys")
        assert not ackredit.get_used_items()
    report = restored.chemical_states.get_preparation_history()[0]["report"]
    assert report["software"] == second["report"]["software"]
    json.dumps(second["template_provenance"], allow_nan=False)


def test_optional_attribution_failure_does_not_erase_completed_reference_chemistry(
    monkeypatch,
):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    def unavailable():
        raise RuntimeError("declared attribution provider failure")

    monkeypatch.setattr(_ackredit, "backend", unavailable)
    with pytest.warns(AckreditTrackingWarning):
        result = msm.physchem.get_chemical_template("BTN", DATA / "BTN.cif")
    assert result["report"]["status"] == "constructed"
    assert result["template"].get_n_atoms() == 16
    assert result["report"]["attribution"]["items"]
    history = result["template"].chemical_states.get_preparation_history()
    assert history[-1]["report"]["source"] == result["report"]["source"]
