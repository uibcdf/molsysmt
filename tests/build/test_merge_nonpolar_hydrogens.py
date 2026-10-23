"""Checking a molecular transform, its source maps and original charge provenance."""

import hashlib
import pickle

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def declared_methanol():
    from molsysmt.native import MolSys, Structures, Topology

    top = Topology(n_atoms=6)
    top.atoms["atom_id"] = ["17", "3", "45", "90", "7", "11"]
    # Deliberately misleading names: chemistry/labels, never names, own policy.
    top.atoms["atom_name"] = ["C", "O", "HD", "N", "O", "C"]
    top.atoms["atom_type"] = ["C", "O", "H", "H", "H", "H"]
    top.bonds = pd.DataFrame(
        {
            "atom1_index": [0, 0, 0, 0, 1],
            "atom2_index": [1, 2, 3, 4, 5],
            "bond_type": ["covalent"] * 5,
            "bond_order": [1] * 5,
        }
    )
    for name, values in {
        "formal_charge": [0] * 6,
        "n_unpaired_electrons": [0] * 6,
        "n_explicit_hydrogens": [0] * 6,
        "n_implicit_hydrogens": [0] * 6,
        "allows_implicit_hydrogens": [True] * 6,
    }.items():
        top._set_chemical_state_atom_attribute(name, values)
    top._chemical_states[0].connectivity_completeness = "complete"
    structures = Structures()
    structures.append(
        coordinates=msm.pyunitwizard.quantity(np.arange(54).reshape(3, 6, 3) / 10, "nm")
    )
    source = MolSys()
    source.topology, source.structures = top, structures
    source.molecular_mechanics.atom_ff_type = ["C", "OA", "H", "H", "H", "HD"]
    source.molecular_mechanics.partial_charge = [-0.4, -0.5, 0.1, 0.2, 0.3, 0.3]
    return source


def merge(source, **kwargs):
    return msm.build.merge_nonpolar_hydrogens(
        source, typing_scheme="autodock4", **kwargs
    )


def unchanged(source, before):
    """Compare stored scientific state, allowing read-only pandas access caches."""
    import json

    for first, second in (
        (source.topology.atoms, before.topology.atoms),
        (
            source.chemical_states._states[0].bonds,
            before.chemical_states._states[0].bonds,
        ),
        (
            source.chemical_states._states[0].atom_attributes,
            before.chemical_states._states[0].atom_attributes,
        ),
        (source.molecular_mechanics.atoms_ff, before.molecular_mechanics.atoms_ff),
    ):
        pd.testing.assert_frame_equal(first, second, check_frame_type=False)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(before.structures.coordinates, to_unit="nm"),
    )

    def normalize(value):
        return json.dumps(
            value,
            sort_keys=True,
            default=lambda item: (
                item.tolist() if hasattr(item, "tolist") else str(item)
            ),
        )

    for name in ("partial_charge_assignment", "atom_type_assignment"):
        assert normalize(getattr(source.molecular_mechanics, name)) == normalize(
            getattr(before.molecular_mechanics, name)
        )


def test_projection_has_direct_and_merged_maps_without_mutating_source():
    source = declared_methanol()
    before = source.copy()
    result = merge(source, structure_indices=[2, 0], return_report=True)
    output, report = result["molecular_system"], result["report"]
    unchanged(source, before)
    assert report["schema"] == "molsysmt.atom_projection@1"
    assert report["output_to_source_atom_indices"].tolist() == [0, 1, 5]
    assert report["source_to_output_atom_indices"].tolist() == [0, 1, -1, -1, -1, 2]
    assert report["source_atom_status"].tolist() == [
        "retained",
        "retained",
        "merged",
        "merged",
        "merged",
        "retained",
    ]
    assert report["merged_source_atom_pairs"].tolist() == [[2, 0], [3, 0], [4, 0]]
    np.testing.assert_allclose(report["charge_transfers"], [0.1, 0.2, 0.3])
    assert report["charge_unit"] == "elementary_charge"
    np.testing.assert_allclose(
        np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
        [0.2, -0.5, 0.3],
    )
    assert output.topology.atoms.atom_id.tolist() == ["17", "3", "11"]
    assert output.molecular_mechanics.atom_ff_type.tolist() == ["C", "OA", "HD"]
    assert msm.get(output, selection=[0], n_explicit_hydrogens=True) == [3]
    assert report["source_structure_indices"].tolist() == [2, 0]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm")[[2, 0]][
            :, [0, 1, 5]
        ],
    )
    report["output_to_source_atom_indices"][0] = 99
    assert output.topology.atoms.atom_id.iloc[0] == "17"


def test_selection_accounts_for_exclusion_separately_from_merging():
    result = merge(declared_methanol(), selection=[4, 0, 2, 4], return_report=True)
    report = result["report"]
    assert report["selected_source_atom_indices"].tolist() == [0, 2, 4]
    assert report["omitted_source_atom_indices"].tolist() == [1, 3, 5]
    assert report["merged_source_atom_pairs"].tolist() == [[2, 0], [4, 0]]
    assert report["output_to_source_atom_indices"].tolist() == [0]
    assert report["selected_total_charge"] == pytest.approx(0)
    assert report["output_total_charge"] == pytest.approx(0)
    with pytest.raises(StructuralInconsistencyError, match="retained heavy parent"):
        merge(declared_methanol(), selection=[2])


@pytest.mark.parametrize(
    "problem",
    [
        "unknown_inventory",
        "virtual_on_H",
        "isotope",
        "charge",
        "radical",
        "label",
        "forcefield",
        "incomplete",
        "nan",
    ],
)
def test_unsupported_or_unassessed_input_fails_without_source_changes(problem):
    source = declared_methanol()
    state = source.chemical_states._states[0]
    if problem == "unknown_inventory":
        state.atom_attributes.loc[0, "n_explicit_hydrogens"] = pd.NA
    elif problem == "virtual_on_H":
        state.atom_attributes.loc[2, "n_explicit_hydrogens"] = 1
    elif problem == "isotope":
        source.topology.atoms.loc[2, "isotope"] = 2
    elif problem == "charge":
        state.atom_attributes.loc[2, "formal_charge"] = 1
    elif problem == "radical":
        state.atom_attributes.loc[2, "n_unpaired_electrons"] = 1
    elif problem == "label":
        source.molecular_mechanics.atom_ff_type = ["H", "OA", "H", "H", "H", "HD"]
    elif problem == "forcefield":
        source.molecular_mechanics.forcefield = "unqualified_all_atom_model"
    elif problem == "incomplete":
        state.connectivity_completeness = "partial"
    else:
        source.molecular_mechanics.partial_charge = [np.nan] * 6
    before = source.copy()
    with pytest.raises(StructuralInconsistencyError):
        merge(source)
    unchanged(source, before)


def test_polar_label_is_retained_even_when_names_suggest_nonpolar():
    source = declared_methanol()
    source.molecular_mechanics.atom_ff_type = ["C", "OA", "HD", "H", "H", "HD"]
    report = merge(source, return_report=True)["report"]
    assert report["output_to_source_atom_indices"].tolist() == [0, 1, 2, 5]


def test_named_calculation_and_typing_are_inherited_as_derived_provenance(tmp_path):
    from tests.build.test_assign_autodock_atom_types import prepared

    source = msm.build.assign_autodock_atom_types(
        prepared("CO"), typing_scheme="autodock4"
    )
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    original = source.copy()
    output = merge(source)
    assignment = output.molecular_mechanics.partial_charge_assignment
    assert assignment["status"] == "derived"
    assert assignment["method"] == "nonpolar_hydrogen_charge_aggregation"
    assert assignment["source_assignment"]["method"] == "gasteiger_marsili"
    assert (
        assignment["source_assignment"]["software"]
        == source.molecular_mechanics.partial_charge_assignment["software"]
    )
    assert output.molecular_mechanics.atom_type_assignment["status"] == "derived"
    unchanged(source, original)
    np.testing.assert_allclose(
        np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
        [0.19000057917, -0.39963024356, 0.20962966439],
        atol=1e-10,
    )
    for restored in [output, output.copy(), pickle.loads(pickle.dumps(output))]:
        msm.convert(
            restored, to_form=tmp_path / "prepared.pdbqt", typing_scheme="autodock4"
        )
        assert (
            restored.molecular_mechanics.partial_charge_assignment["source_assignment"][
                "method"
            ]
            == "gasteiger_marsili"
        )
    # The binding follows the derived values; stale edits cannot be legitimized.
    output.molecular_mechanics.atoms_ff.loc[0, "partial_charge"] += 0.1
    with pytest.raises(StructuralInconsistencyError):
        msm.convert(output, to_form=tmp_path / "bad.pdbqt", typing_scheme="autodock4")


def test_public_form_agnostic_route_and_nondefault_units():
    source = declared_methanol()
    domains = [
        source.topology,
        source.structures,
        source.molecular_mechanics,
    ]
    with msm.pyunitwizard.context(standard_units=["pm", "coulomb"]):
        source.structures.coordinates = msm.pyunitwizard.convert(
            source.structures.coordinates, to_unit="angstrom"
        )
        output = merge(source)
        other = merge(domains)
        np.testing.assert_allclose(
            np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
            np.asarray(other.molecular_mechanics.partial_charge, dtype=float),
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
            msm.pyunitwizard.get_value(other.structures.coordinates, to_unit="nm"),
        )


def test_completed_writer_map_records_actual_tree_order_and_rounding(tmp_path):
    from tests.form.file_pdbqt.test_native_contract import LIGAND

    path = tmp_path / "ligand.pdbqt"
    path.write_text(LIGAND)
    source = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    tree = msm.form.file_pdbqt.get_torsion_tree(path)
    tree["fragment_atom_indices"][:2] = tree["fragment_atom_indices"][:2][::-1]
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=tree,
        return_atom_map=True,
    )
    assert mapping["output_to_source_atom_indices"].tolist() == [1, 0, 2, 3]
    assert mapping["source_to_output_atom_indices"].tolist() == [1, 0, 2, 3]
    assert mapping["ordered_root_source_atom_indices"].tolist() == [1, 0]
    assert mapping["first_root_source_atom_index"] == 1
    assert (
        mapping["payload_sha256"]
        == hashlib.sha256(text.removeprefix("pdbqt_text:").encode()).hexdigest()
    )
    assert mapping["charge_unit"] == "elementary_charge"
    assert (
        abs(mapping["written_total_charge"] - mapping["total_charge_before_rounding"])
        <= mapping["charge_rounding_error_bound"] + 1e-12
    )
    output = tmp_path / "mapped.pdbqt"
    destination, file_map = msm.convert(
        source,
        to_form=output,
        typing_scheme="autodock4",
        torsion_tree=tree,
        return_atom_map=True,
    )
    assert destination == output
    assert file_map["payload_sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()
    np.testing.assert_array_equal(
        file_map["output_to_source_atom_indices"],
        mapping["output_to_source_atom_indices"],
    )


def test_writer_selection_map_uses_full_input_axis_and_can_compose_projection():
    source = declared_methanol()
    source.structures = source.structures.extract(structure_indices=[0])
    projection = merge(source, return_report=True)
    text, export = msm.convert(
        projection["molecular_system"],
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        selection=[2, 0],
        return_atom_map=True,
    )
    assert export["output_to_source_atom_indices"].tolist() == [0, 2]
    assert export["source_to_output_atom_indices"].tolist() == [0, -1, 1]
    original = projection["report"]["output_to_source_atom_indices"][
        export["output_to_source_atom_indices"]
    ]
    assert original.tolist() == [0, 5]
    assert "ATOM" in text


def test_writer_map_does_not_invent_labels_for_unknown_omitted_atoms():
    source = declared_methanol()
    source.topology.atoms.loc[1, ["atom_id", "atom_name", "atom_type"]] = pd.NA
    _, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        selection=[0],
        structure_indices=[0],
        typing_scheme="autodock4",
        return_atom_map=True,
    )
    assert mapping["source_atom_ids"][1] is None
    assert mapping["source_atom_names"][1] is None
    assert mapping["source_atom_types"][1] is None
    assert mapping["source_to_output_atom_indices"].tolist() == [0, -1, -1, -1, -1, -1]


def test_bad_public_options_are_rejected():
    with pytest.raises(ArgumentError):
        msm.build.merge_nonpolar_hydrogens(declared_methanol(), typing_scheme="unknown")
    with pytest.raises(ArgumentError):
        merge(declared_methanol(), return_report="yes")


def test_reference_attribution_is_observed_and_loading_does_not_recredit(monkeypatch):
    ackredit = pytest.importorskip("ackredit")
    from molsysmt import _ackredit

    source = declared_methanol()
    reference = "meeko-terminal-charge-aggregation-reference"
    with ackredit.session("typed-projection"):
        with ackredit.capture("first") as first:
            result = merge(source, return_report=True)
        with ackredit.capture("second") as second:
            merge(source)
        for capture in [first, second]:
            uses = capture.attribution.to_dict()["uses"]
            assert any(
                use["item_id"] == reference
                and use["roles"] == ["reference_implementation"]
                for use in uses
            )
    saved = pickle.dumps(result)
    with ackredit.session("reader"):
        restored = pickle.loads(saved)
        assert restored["report"]["attribution"] == result["report"]["attribution"]
        assert not ackredit.get_used_items()
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    absent = merge(source, return_report=True)
    np.testing.assert_allclose(
        msm.get(absent["molecular_system"], partial_charge=True),
        msm.get(result["molecular_system"], partial_charge=True),
    )
    assert absent["report"]["references"] == result["report"]["references"]


def test_merge_clears_reduced_analyses_and_retains_original_coverage():
    source = declared_methanol()
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=6,
        n_structures=3,
        evaluated_structure_indices=[0, 2],
        method="synthetic",
    )
    source.interactions = {"existing": analysis}
    result = merge(source, return_report=True)
    assert not result["molecular_system"].interactions
    assert result["report"]["invalidated_interaction_names"] == ["existing"]
    assert source.interactions["existing"].evaluated_structure_indices.tolist() == [
        0,
        2,
    ]
    assert msm.get(
        result["molecular_system"], selection=[0], allows_implicit_hydrogens=True
    ) == [False]


def test_projection_is_json_portable_without_per_atom_python_objects():
    import json

    result = merge(declared_methanol(), return_report=True)
    report = result["report"]
    restored = json.loads(json.dumps(report, default=lambda item: item.tolist()))
    assert restored["source_to_output_atom_indices"] == [0, 1, -1, -1, -1, 2]
    assert restored["charge_unit"] == "elementary_charge"
    assert restored["references"][0]["roles"] == ["reference_implementation"]


@pytest.mark.parametrize("case_name", ["1iep", "5x72-p59", "5x72-p69"])
def test_original_vina_ligands_have_type_driven_maps_and_conserved_charge(case_name):
    import json
    from pathlib import Path

    Chem = pytest.importorskip("rdkit.Chem")
    root = Path(__file__).parents[1] / "form/data/vina_examples"
    record = next(
        record
        for record in json.loads((root / "manifest.json").read_text())["records"]
        if record["name"] == case_name
    )
    path = root / record["files"]["sdf"]["filename"]
    assert (
        hashlib.sha256(path.read_bytes()).hexdigest()
        == record["files"]["sdf"]["sha256"]
    )
    molecule = Chem.SDMolSupplier(str(path), removeHs=False)[0]
    assert molecule is not None
    source = msm.build.assign_autodock_atom_types(molecule, typing_scheme="autodock4")
    source.molecular_mechanics.partial_charge = (
        np.arange(source.get_n_atoms(), dtype=float) / 100
    )
    result = merge(source, return_report=True)
    report, output = result["report"], result["molecular_system"]
    assert output.get_n_atoms() == (40 if case_name == "1iep" else 25)
    assert len(report["merged_source_atom_pairs"]) == (
        29 if case_name == "1iep" else 14
    )
    assert report["selected_total_charge"] == pytest.approx(
        report["output_total_charge"], abs=report["charge_conservation_tolerance"]
    )
    assert len(report["source_atom_status"]) == source.get_n_atoms()
    # Source positions, not names, explain each retained atom and coordinate.
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="angstrom"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="angstrom")[
            :, report["output_to_source_atom_indices"]
        ],
    )


def test_user_guide_examples_execute_as_one_workflow():
    import re
    from pathlib import Path

    guide = (
        Path(__file__).parents[2]
        / "docs/content/user/tools/build/merge_nonpolar_hydrogens.md"
    )
    namespace = {}
    for block in re.findall(r"```python\n(.*?)```", guide.read_text(), flags=re.S):
        exec(compile(block, str(guide), "exec"), namespace)
    assert namespace["restored_report"]["n_output_atoms"] == 14


def test_ready_native_projection_does_not_load_optional_chemical_engines():
    import subprocess
    import sys

    script = r"""
import importlib.abc
import importlib.machinery
import sys
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol, merge
import molsysmt as msm
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
result = merge(declared_methanol(), structure_indices=[0], return_report=True)
text, exported = msm.convert(result["molecular_system"], to_form="string:pdbqt_text",
    typing_scheme="autodock4", return_atom_map=True)
assert len(exported["output_to_source_atom_indices"]) == 3
assert not attempted, attempted
assert not roots.intersection(name.split(".")[0] for name in sys.modules)
"""
    completed = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
