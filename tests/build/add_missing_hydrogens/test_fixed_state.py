"""Checking fixed-state H geometry against independent molecular expectations."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

Chem = pytest.importorskip("rdkit.Chem")
puw = msm.pyunitwizard


def prepared(smiles, positions):
    molecule = Chem.MolFromSmiles(smiles)
    conf = Chem.Conformer(molecule.GetNumAtoms())
    conf.SetPositions(np.asarray(positions, dtype=float))
    conf.Set3D(True)
    molecule.AddConformer(conf)
    return msm.convert(molecule, to_form="molsysmt.MolSys")


def hydrogenate(source, **kwargs):
    return msm.build.add_missing_hydrogens(
        source,
        pH=None,
        engine="RDKit",
        mode="fixed_chemical_state",
        return_report=True,
        **kwargs,
    )


@pytest.mark.parametrize(
    "smiles,positions,count,charge",
    [
        ("C", [[0, 0, 0]], 4, 0),
        ("CCO", [[0, 0, 0], [1.5, 0, 0], [2.05, 1.3, 0]], 6, 0),
        ("[NH4+]", [[0, 0, 0]], 4, 1),
        ("CS", [[0, 0, 0], [1.8, 0, 0]], 4, 0),
        (
            "CP(=O)(O)O",
            [
                [0, 0, 0],
                [1.8, 0, 0],
                [2.3, 1.3, 0],
                [2.3, -0.8, 1.2],
                [2.3, -0.8, -1.2],
            ],
            5,
            0,
        ),
    ],
)
def test_inventory_charge_geometry_units_and_exact_pose(
    smiles, positions, count, charge
):
    source = prepared(smiles, positions)
    before = source.copy()
    with puw.context(standard_units=["pm", "fs"]):
        result = hydrogenate(source)
    output, report = result["molecular_system"], result["report"]
    n = source.get_n_atoms()
    assert output.get_n_atoms() == n + count
    assert report["n_added_hydrogens"] == count
    assert report["parameters"]["pH"] is None
    assert report["method"] == "local_hydrogen_placement"
    assert report["software"]["rdkit"]
    assert report["attribution"]["items"]
    assert report["parent_hydrogen_pairs"].shape == (count, 2)
    np.testing.assert_array_equal(
        report["atom_correspondence"], np.column_stack((np.arange(n), np.arange(n)))
    )
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm")[:, :n],
        puw.get_value(source.structures.coordinates, to_unit="nm"),
    )
    assert puw.get_unit(output.structures.coordinates) == puw.get_unit(
        source.structures.coordinates
    )
    assert (
        int(output.chemical_states._states[0].atom_attributes["formal_charge"].sum())
        == charge
    )
    inventory = msm.physchem.get_hydrogen_inventory(output)
    assert inventory["status"] == "available"
    assert inventory["missing_hydrogen_counts"].tolist() == [0] * (n + count)
    xyz = puw.get_value(output.structures.coordinates, to_unit="angstrom")[0]
    for parent, h in report["parent_hydrogen_pairs"]:
        # Independent broad chemical intervals, not RDKit-derived expected values.
        low, high = {
            "C": (1.0, 1.15),
            "N": (0.95, 1.1),
            "O": (0.9, 1.05),
            "S": (1.25, 1.45),
        }[source.topology.atoms.at[parent, "atom_type"]]
        assert low < np.linalg.norm(xyz[h] - xyz[parent]) < high


def test_methane_is_tetrahedral_and_idempotent():
    source = prepared("C", [[1.2, -0.7, 2.3]])
    first = hydrogenate(source)
    full = first["molecular_system"]
    xyz = puw.get_value(full.structures.coordinates, to_unit="angstrom")[0]
    vectors = xyz[1:] - xyz[0]
    cosines = (
        vectors
        @ vectors.T
        / np.outer(np.linalg.norm(vectors, axis=1), np.linalg.norm(vectors, axis=1))
    )
    np.testing.assert_allclose(cosines[np.triu_indices(4, 1)], -1 / 3, atol=0.015)
    full.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=5,
            n_structures=1,
            evaluated_structure_indices=[0],
            method="example",
        )
    }
    second = hydrogenate(full)
    assert second["report"]["n_added_hydrogens"] == 0
    assert second["report"]["status"] == "unchanged"
    assert second["report"]["parent_hydrogen_pairs"].shape == (0, 2)
    pd.testing.assert_frame_equal(
        second["molecular_system"].topology.atoms, full.topology.atoms
    )
    np.testing.assert_array_equal(
        second["molecular_system"].interactions["empty"].evaluated_structure_indices,
        [0],
    )
    np.testing.assert_array_equal(
        puw.get_value(second["molecular_system"].structures.coordinates),
        puw.get_value(full.structures.coordinates),
    )


def test_partial_hydrogens_isotope_and_permutation_are_preserved():
    source = prepared("[2H]C", [[1.09, 0, 0], [0, 0, 0]])
    source.topology.atoms["atom_id"] = pd.array(["same", "same"], dtype="string")
    result = hydrogenate(source)
    output = result["molecular_system"]
    assert output.get_n_atoms() == 5
    assert result["report"]["n_added_hydrogens"] == 3
    assert output.topology.atoms.iloc[0]["isotope"] == 2
    assert output.topology.atoms["atom_id"].iloc[:2].tolist() == ["same", "same"]
    assert result["report"]["parent_hydrogen_pairs"][:, 0].tolist() == [1, 1, 1]
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates)[:, :2],
        puw.get_value(source.structures.coordinates),
    )


@pytest.mark.parametrize(
    "defect",
    [
        "missing_counts",
        "wrong_count",
        "radical",
        "metal",
        "disconnected",
        "coincident",
        "missing_charge",
        "partial_graph",
    ],
)
def test_unresolved_or_unsupported_inputs_fail_without_changing_source(defect):
    source = prepared("CC", [[0, 0, 0], [1.5, 0, 0]])
    state = source.chemical_states._states[0]
    if defect == "missing_counts":
        state.atom_attributes.loc[0, "n_implicit_hydrogens"] = pd.NA
    elif defect == "wrong_count":
        state.atom_attributes.loc[0, "n_implicit_hydrogens"] = 2
    elif defect == "radical":
        state.atom_attributes.loc[0, "n_unpaired_electrons"] = 1
    elif defect == "metal":
        source.topology.atoms.loc[0, "atom_type"] = "Zn"
    elif defect == "disconnected":
        state.bonds = state.bonds.iloc[:0].copy()
    elif defect == "coincident":
        source.structures.coordinates = puw.quantity(np.zeros((1, 2, 3)), "nm")
    elif defect == "missing_charge":
        state.atom_attributes.loc[0, "formal_charge"] = pd.NA
    elif defect == "partial_graph":
        state.connectivity_completeness = "partial"
    before = source.copy()
    with pytest.raises(StructuralInconsistencyError):
        hydrogenate(source)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates),
        puw.get_value(before.structures.coordinates),
    )


def test_periodic_compact_pose_box_and_frame_link_and_split_rejection():
    source = prepared("CC", [[0, 0, 0], [1.5, 0, 0]])
    source.structures.box = puw.quantity(np.eye(3)[None] * 2.0, "nm")
    msm.set(source, structure_chemical_state_index=[0])
    result = hydrogenate(source, chemical_state="structure", structure_indices=[0])
    np.testing.assert_array_equal(
        puw.get_value(result["molecular_system"].structures.box),
        puw.get_value(source.structures.box),
    )
    np.testing.assert_array_equal(
        result["molecular_system"]._structure_chemical_state_indices, [0]
    )
    source.structures.coordinates = puw.quantity([[[0.0, 0, 0], [1.85, 0, 0]]], "nm")
    with pytest.raises(
        StructuralInconsistencyError, match="split across periodic images"
    ):
        hydrogenate(source)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(pH=7.4, engine="RDKit", mode="fixed_chemical_state"),
        dict(pH=None, engine="MolSysMT", mode="fixed_chemical_state"),
        dict(pH=None, engine="RDKit"),
        dict(return_report=True),
    ],
)
def test_explicit_mode_cannot_apply_pH_or_fallback(kwargs):
    with pytest.raises(ArgumentError):
        msm.build.add_missing_hydrogens(prepared("C", [[0, 0, 0]]), **kwargs)


def test_real_est_retains_pose_and_five_cip_centers_through_h5msm(tmp_path):
    data = Path(__file__).parents[2] / "physchem" / "data" / "chemical_templates"
    manifest = json.loads((data / "manifest.json").read_text())
    system = msm.convert(data / "1qku.cif.gz", to_form="molsysmt.MolSys")
    ligand = msm.extract(system, selection=manifest["source_selection"])
    source = msm.physchem.apply_chemical_template(
        ligand,
        template=data / "est_template.h5msm",
        atom_correspondence=manifest["atom_correspondence"],
        template_provenance=manifest["template_provenance"],
    )["molecular_system"]
    result = hydrogenate(source)
    output = result["molecular_system"]
    assert output.get_n_atoms() == 44
    assert msm.get(output, n_bonds=True) == 47
    assert result["report"]["n_added_hydrogens"] == 24
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates)[:, :20],
        puw.get_value(source.structures.coordinates),
    )
    expected = [
        manifest["expected_stereo"][name] for name in manifest["source_atom_names"]
    ]
    cip = msm.physchem.get_cip_stereochemistry(output, from_coordinates=True)
    np.testing.assert_array_equal(cip["atom_stereochemistry"][:20], expected)
    sites = msm.physchem.get_hbond_sites(output)
    assert sites["donor_hydrogen_pairs"][:, 0].tolist() == [3, 18]
    assert sites["acceptor_atom_indices"].tolist() == [3, 18]
    path = tmp_path / "est_with_h.h5msm"
    msm.convert(output, to_form="file:h5msm", output_filename=str(path))
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.get_n_atoms() == 44
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes,
        output.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        puw.get_value(loaded.structures.coordinates),
        puw.get_value(output.structures.coordinates),
    )


def test_phenol_hydrogens_are_in_ring_plane_and_oh_is_generated():
    phase = np.arange(6) * np.pi / 3
    ring = 1.4 * np.column_stack((np.cos(phase), np.sin(phase), np.zeros(6)))
    source = prepared("Oc1ccccc1", np.vstack(([2.75, 0, 0], ring)))
    result = hydrogenate(source)
    output = result["molecular_system"]
    assert result["report"]["n_added_hydrogens"] == 6
    xyz = puw.get_value(output.structures.coordinates, to_unit="angstrom")[0]
    for parent, h in result["report"]["parent_hydrogen_pairs"]:
        if parent != 0:
            assert abs(xyz[h, 2]) < 1e-8
            assert np.linalg.norm(xyz[h, :2]) > np.linalg.norm(xyz[parent, :2])
    assert msm.physchem.get_hbond_sites(output)["donor_hydrogen_pairs"][
        :, 0
    ].tolist() == [0]


def test_full_analysis_occurrences_are_invalidated_only_on_added_copy():
    source = prepared("CCO", [[0, 0, 0], [1.5, 0, 0], [2.05, 1.3, 0]])
    source.interactions = {
        "test": msm.Interactions.from_records(
            [
                dict(
                    structure_index=0,
                    interaction_type="pair",
                    participants=[
                        dict(role="first", atom_indices=[0]),
                        dict(role="second", atom_indices=[2]),
                    ],
                )
            ],
            n_atoms=3,
            n_structures=1,
            evaluated_structure_indices=[0],
            method="example",
        )
    }
    output = hydrogenate(source)
    assert output["report"]["invalidated_interactions"] == ["test"]
    assert (
        output["molecular_system"]
        .interactions["test"]
        .query(structure_indices=[0])
        .n_interactions
        == 0
    )
    assert (
        output["molecular_system"].interactions["test"].evaluated_structure_indices.size
        == 0
    )
    assert source.interactions["test"].n_interactions == 1


def test_multiple_frames_and_states_require_explicit_extraction():
    source = prepared("C", [[0, 0, 0]])
    source.structures.append(coordinates=puw.quantity([[[0, 0, 0.1]]], "nm"))
    with pytest.raises(StructuralInconsistencyError, match="Extract exactly one"):
        hydrogenate(source, structure_indices=[0])
    single = prepared("C", [[0, 0, 0]])
    single.chemical_states.append_state()
    with pytest.raises(StructuralInconsistencyError, match="Extract exactly one"):
        hydrogenate(single, chemical_state=0)


def test_h5_input_form_and_default_native_output(tmp_path):
    source = prepared("CCO", [[0, 0, 0], [1.5, 0, 0], [2.05, 1.3, 0]])
    path = tmp_path / "prepared.h5msm"
    msm.convert(source, to_form="file:h5msm", output_filename=str(path))
    output = msm.build.add_missing_hydrogens(
        path, pH=None, engine="RDKit", mode="fixed_chemical_state"
    )
    assert msm.get_form(output) == "molsysmt.MolSys"
    assert output.get_n_atoms() == 9
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates)[:, :3],
        puw.get_value(source.structures.coordinates),
    )


def test_optional_attribution_failure_and_absence_preserve_completed_result(
    monkeypatch,
):
    import warnings

    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    def broken():
        raise RuntimeError("hydrogen credit failure")

    source = prepared("C", [[0, 0, 0]])
    for provider in (lambda: None, broken):
        monkeypatch.setattr(_ackredit, "backend", provider)
        with warnings.catch_warnings():
            warnings.simplefilter("error", AckreditTrackingWarning)
            output = hydrogenate(source)
        assert output["molecular_system"].get_n_atoms() == 5
        assert output["report"]["attribution"]["items"]


def test_real_ackredit_enclosing_scope_records_executed_software_and_cip():
    ackredit = pytest.importorskip("ackredit")
    source = prepared("C", [[0, 0, 0]])
    with ackredit.session("preparation-control"):
        with ackredit.scope("pharmacophoremt.prepare"):
            result = hydrogenate(source)
        used = ackredit.get_used_items()
        for item in result["report"]["attribution"]["items"]:
            assert item["id"] in used
        tree = ackredit.current_session().usage_tree
        assert (
            "molsysmt.build.add_missing_hydrogens"
            in tree["pharmacophoremt.prepare"]["children"]
        )


def test_missing_rdkit_has_no_fallback_and_general_tools_remain_available():
    import subprocess
    import sys

    script = """
import importlib.abc
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'rdkit':
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, Absent())
import molsysmt as msm
b=msm.MolSysBuilder()
b.add_atom(atom_type='C',atom_name='C')
b.set_coordinates(msm.pyunitwizard.quantity([[[0.,0.,0.]]],'nm'))
s=b.build()
r=msm.physchem.get_hydrogen_inventory(s)
assert r['status']=='unassessed'
added=msm.build.add_terminal_atoms(s,[{'parent_atom_index':0,'atom_type':'H'}],
    msm.pyunitwizard.quantity([[[0,0,.109]]],'nm'))
assert added['molecular_system'].get_n_atoms()==2
try:
    msm.build.add_missing_hydrogens(s,mode='fixed_chemical_state',pH=None,engine='RDKit')
except ImportError:
    pass
else:
    raise AssertionError('Missing RDKit did not raise an import diagnostic')
assert 'rdkit' not in sys.modules
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr


def test_declared_methylammonium_charge_inventory_and_tetrahedral_nitrogen():
    source = prepared("C[NH3+]", [[0, 0, 0], [1.5, 0, 0]])
    output = hydrogenate(source)
    assert output["report"]["n_added_hydrogens"] == 6
    assert (
        int(
            output["molecular_system"]
            .chemical_states._states[0]
            .atom_attributes["formal_charge"]
            .sum()
        )
        == 1
    )
    xyz = puw.get_value(
        output["molecular_system"].structures.coordinates, to_unit="nm"
    )[0]
    hs = output["report"]["parent_hydrogen_pairs"]
    hs = hs[hs[:, 0] == 1, 1]
    unit = xyz[hs] - xyz[1]
    unit /= np.linalg.norm(unit, axis=1)[:, None]
    np.testing.assert_allclose(unit @ np.array([-1.0, 0, 0]), -1 / 3, atol=0.015)


def test_absolute_double_bond_stereo_is_retained():
    source = prepared("C/C=C/C", [[-1.5, 1, 0], [0, 0, 0], [1.35, 0, 0], [2.7, -1, 0]])
    result = hydrogenate(source)
    assert result["report"]["n_added_hydrogens"] == 8
    declared = msm.physchem.get_cip_stereochemistry(result["molecular_system"])
    observed = msm.physchem.get_cip_stereochemistry(
        result["molecular_system"], from_coordinates=True
    )
    assert declared["bond_stereochemistry"].tolist().count("E") == 1
    assert observed["bond_stereochemistry"].tolist().count("E") == 1


@pytest.mark.parametrize(
    "defect", ["nonfinite", "missing_coordinates", "unknown_order", "invalid_endpoint"]
)
def test_geometry_and_edge_preflight_are_deliberate_errors(defect):
    source = prepared("CC", [[0, 0, 0], [1.5, 0, 0]])
    state = source.chemical_states._states[0]
    if defect == "nonfinite":
        source.structures.coordinates = puw.quantity(
            [[[np.nan, 0, 0], [0.15, 0, 0]]], "nm"
        )
    elif defect == "missing_coordinates":
        source.structures.coordinates = None
    elif defect == "unknown_order":
        state.bonds.loc[0, "bond_order"] = pd.NA
    else:
        state.bonds = pd.DataFrame(state.bonds).astype({"atom1_index": object})
        state.bonds.loc[0, "atom1_index"] = 0.5
    with pytest.raises(StructuralInconsistencyError):
        hydrogenate(source)
    assert source.get_n_atoms() == 2


def test_backend_failure_is_transactional_and_does_not_fallback(monkeypatch):
    source = prepared("C", [[0, 0, 0]])
    before = source.topology.atoms.copy(deep=True)

    def broken(*args, **kwargs):
        raise RuntimeError("forced coordinate failure")

    monkeypatch.setattr(Chem, "AddHs", broken)
    with pytest.raises(StructuralInconsistencyError, match="forced coordinate failure"):
        hydrogenate(source)
    pd.testing.assert_frame_equal(source.topology.atoms, before)


def test_backend_unit_reinterpretation_is_rejected(monkeypatch):
    source = prepared("CC", [[0, 0, 0], [1.5, 0, 0]])
    original = msm.basic.convert

    def wrong_units(*args, **kwargs):
        molecule = original(*args, **kwargs)
        if kwargs.get("to_form") == "rdkit.Mol":
            conf = molecule.GetConformer()
            conf.SetPositions(conf.GetPositions() / 10.0)
        return molecule

    monkeypatch.setattr(msm.basic, "convert", wrong_units)
    with pytest.raises(StructuralInconsistencyError, match="coordinate units"):
        hydrogenate(source)


def test_mirrored_declared_chiral_pose_is_rejected():
    source = prepared(
        "N[C@@H](C)C(=O)O",
        [
            [-1.4, 0, 0],
            [0, 0, 0],
            [0.4, 1.2, 0.9],
            [0.5, -1.2, 0.3],
            [1.7, -1.3, 0.3],
            [-0.1, -2.3, 0.3],
        ],
    )
    # One of a pose and its reflection contradicts the same declared S center.
    rejected = 0
    for sign in [1.0, -1.0]:
        test = source.copy()
        xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
        xyz[..., 0] *= sign
        test.structures.coordinates = puw.quantity(xyz, "nm")
        try:
            hydrogenate(test)
        except StructuralInconsistencyError as error:
            assert "stereochemistry" in str(error)
            rejected += 1
    assert rejected == 1


def test_fresh_portable_attribution_reader_keeps_producer_versions_without_backends(
    tmp_path,
):
    import subprocess
    import sys

    result = hydrogenate(prepared("C", [[0, 0, 0]]))
    record = dict(
        software=result["report"]["software"],
        attribution=result["report"]["attribution"],
    )
    path = tmp_path / "preparation_attribution.json"
    path.write_text(json.dumps(record))
    script = """
import importlib.abc
import json
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit', 'ackredit'}:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, Absent())
record=json.load(open(sys.argv[1]))
for name,version in record['software'].items():
    assert any(item['id']==f'software:{name}:{version}' for item in record['attribution']['items'])
assert 'rdkit' not in sys.modules and 'ackredit' not in sys.modules
print(record['software']['rdkit'])
"""
    run = subprocess.run(
        [sys.executable, "-c", script, str(path)], capture_output=True, text=True
    )
    assert run.returncode == 0, run.stderr
    assert run.stdout.strip() == record["software"]["rdkit"]


def test_excess_existing_hydrogens_are_rejected_without_removal():
    b = msm.MolSysBuilder()
    b.add_atom(atom_type="C", atom_name="C")
    for i in range(5):
        b.add_atom(atom_type="H", atom_name=f"H{i}")
        b.add_bond(0, i + 1, bond_order=1, bond_type="covalent")
    b.set_coordinates(
        puw.quantity(
            [
                [
                    [0, 0, 0],
                    [0.109, 0, 0],
                    [-0.109, 0, 0],
                    [0, 0.109, 0],
                    [0, -0.109, 0],
                    [0, 0, 0.109],
                ]
            ],
            "nm",
        )
    )
    source = b.build()
    state = source.chemical_states._states[0]
    state.connectivity_completeness = "complete"
    state.bonds["is_aromatic"] = pd.array([False] * 5, dtype="boolean")
    for name, value in dict(
        formal_charge=0,
        is_aromatic=False,
        n_unpaired_electrons=0,
        n_implicit_hydrogens=0,
        n_explicit_hydrogens=0,
        allows_implicit_hydrogens=False,
    ).items():
        source.topology._set_chemical_state_atom_attribute(name, [value] * 6)
    before = source.topology.atoms.copy(deep=True)
    with pytest.raises(StructuralInconsistencyError):
        hydrogenate(source)
    pd.testing.assert_frame_equal(source.topology.atoms, before)
    assert source.get_n_atoms() == 6
