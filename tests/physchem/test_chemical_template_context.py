"""Protecting chemical assignment with declared polymer context and original axes."""

import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Structures
from tests.native.test_preparation_history import assert_tree
from tests.physchem import test_chemical_template_est as est_controls
from tests.physchem.test_chemical_template import PROVENANCE, _source, _stereo_template

DATA = est_controls.DATA
est_case = est_controls.est_case


def peptide_case(names=None, **choices):
    definition = msm.physchem.get_peptide_chemical_template(
        ["GLY", "GLY", "GLY"] if names is None else names,
        "ammonium",
        "carboxylate",
        **choices,
    )
    template = definition["template"]
    source = template.copy()
    state = source.chemical_states._states[0]
    for column in state.atom_attributes:
        state.atom_attributes[column] = pd.NA
    for field in (
        "bond_order",
        "fractional_bond_order",
        "is_aromatic",
        "is_conjugated",
    ):
        state.bonds[field] = pd.NA
    state._normalize_atom_attribute_columns()
    state.connectivity_completeness = "partial"
    n_atoms = source.get_n_atoms()
    source.structures = Structures()
    source.structures.append(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(6 * n_atoms).reshape(2, n_atoms, 3) / 100, "nm"
        ),
        time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"),
    )
    source.interactions = {
        "old": msm.Interactions.from_records(
            [],
            n_atoms=n_atoms,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="control",
        )
    }
    source.chemical_states._append_state(template.chemical_states._states[0].copy())
    selected = msm.select(source, selection="group_index == 1")
    pairs = source.chemical_states.get_bonds()[["atom1_index", "atom2_index"]].to_numpy(
        dtype=np.int64
    )
    incident = np.isin(pairs, selected).any(axis=1)
    context = np.setdiff1d(pairs[incident], selected)
    options = dict(
        template=template,
        template_provenance=definition["template_provenance"],
        selection=selected,
        atom_correspondence=np.column_stack((selected, selected)),
        context_atom_correspondence=np.column_stack((context, context)),
    )
    return source, options


@pytest.mark.parametrize("form", ["native", "topology", "h5msm"])
def test_internal_residue_uses_polymer_context_without_creating_cut_termini(
    tmp_path, form
):
    source, options = peptide_case()
    before = source.copy()
    selected = options["selection"]
    outside = np.setdiff1d(np.arange(source.get_n_atoms()), selected)
    # Reference indices differ from source indices; the declared maps decide correspondence.
    permutation = np.arange(source.get_n_atoms())[::-1]
    reference = options["template"].copy()
    reference.topology.atoms = reference.topology.atoms.iloc[permutation].reset_index(
        drop=True
    )
    reference.chemical_states = reference.chemical_states._extract_atoms(permutation)
    options["template"] = reference
    options["atom_correspondence"][:, 0] = permutation[selected]
    options["context_atom_correspondence"][:, 0] = permutation[
        options["context_atom_correspondence"][:, 1]
    ]
    options["selection"] = "group_index == 1"
    molecular_system = source if form == "native" else source.topology
    expected_bonds = before.chemical_states._states[0].bonds
    if form == "h5msm":
        molecular_system = tmp_path / "source.h5msm"
        msm.convert(source, to_form=molecular_system)
        # Compare against the public input interpretation, including its null dtypes.
        expected_bonds = msm.h5msm.read_layers(
            molecular_system, layers=["chemical_states"]
        )["chemical_states"].get_bonds()
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        assessment = msm.physchem.assess_chemical_template(molecular_system, **options)
        assert assessment["status"] == "compatible", assessment["issues"]
        output = msm.physchem.apply_chemical_template(molecular_system, **options)
    result, report = output["molecular_system"], output["report"]
    state = result.chemical_states._states[0]
    assert report["rule_version"] == 5
    assert report["coverage"]["scope"] == "selected_with_context"
    assert report["coverage"]["boundary"] == "declared_mapped_context"
    assert report["coverage"]["graph"] == "same_stored_relationships"
    assert report["coverage"]["external_source_bond_indices"].size == 2
    assert report["coverage"]["unmapped_template_atom_indices"].size == 7
    assert state.connectivity_completeness == "partial"
    assert report["added_bonds"] == []
    assert all(
        record["index"] in selected
        for record in report["assigned_fields"]
        if record["axis"] == "atom"
    )
    assert all(
        record["index"] not in outside
        for record in report["assigned_fields"]
        if record["axis"] == "atom"
    )
    for field in ("formal_charge", "n_explicit_hydrogens", "allows_implicit_hydrogens"):
        assert (
            state.atom_attributes[field].iloc[selected].tolist()
            == before.chemical_states._states[1]
            .atom_attributes[field]
            .iloc[selected]
            .tolist()
        )
    atom_n = source.topology.atoms.index[
        (source.topology.atoms.group_index == 1)
        & (source.topology.atoms.atom_name == "N")
    ][0]
    assert state.atom_attributes.at[atom_n, "formal_charge"] == 0
    assert state.atom_attributes.at[atom_n, "n_explicit_hydrogens"] == 1
    pd.testing.assert_frame_equal(
        state.atom_attributes.iloc[outside],
        before.chemical_states._states[0].atom_attributes.iloc[outside],
    )
    pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    outside_bonds = ~np.isin(pairs, selected).any(axis=1)
    pd.testing.assert_frame_equal(
        state.bonds[outside_bonds],
        expected_bonds[outside_bonds],
        check_like=True,
        check_dtype=False,
    )
    pd.testing.assert_frame_equal(result.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        result.chemical_states._states[1].atom_attributes,
        before.chemical_states._states[1].atom_attributes,
    )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    if form != "topology":
        for field, unit in (("coordinates", "nm"), ("time", "ps")):
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(
                    getattr(result.structures, field), to_unit=unit
                ),
                msm.pyunitwizard.get_value(
                    getattr(before.structures, field), to_unit=unit
                ),
            )
        assert result.interactions["old"].evaluated_structure_indices.size == 0
        assert source.interactions["old"].evaluated_structure_indices.tolist() == [0, 1]
    path = tmp_path / "selected-context.h5msm"
    msm.convert(result, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert_tree(
        loaded.chemical_states.get_preparation_history(),
        result.chemical_states.get_preparation_history(),
    )
    assert_tree(
        loaded.chemical_states.get_preparation_history()[-1]["report"][
            "context_atom_correspondence"
        ],
        options["context_atom_correspondence"],
    )
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_hbond_sites(result, method="smarts_donor_acceptor")


@pytest.mark.parametrize(
    "failure",
    [
        "missing_context",
        "context_conflict",
        "boundary_order",
        "unexpected_edge",
        "completion",
    ],
)
def test_context_failure_is_inspectable_and_transactional(failure):
    source, options = peptide_case()
    state = source.chemical_states._states[0]
    if failure == "missing_context":
        options["context_atom_correspondence"] = options["context_atom_correspondence"][
            1:
        ]
    elif failure == "context_conflict":
        state.atom_attributes.at[
            int(options["context_atom_correspondence"][0, 1]), "formal_charge"
        ] = 1
    elif failure == "boundary_order":
        selected = options["selection"]
        pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
        boundary = np.flatnonzero(np.isin(pairs, selected).sum(axis=1) == 1)[0]
        state.bonds.at[boundary, "bond_order"] = 2
    elif failure == "unexpected_edge":
        # This mapped pair exists in neither the declared template nor its boundary.
        extra = int(
            np.setdiff1d(
                np.arange(source.get_n_atoms()),
                np.r_[
                    options["selection"], options["context_atom_correspondence"][:, 1]
                ],
            )[0]
        )
        options["context_atom_correspondence"] = np.r_[
            options["context_atom_correspondence"], [[extra, extra]]
        ]
        added = state.bonds.iloc[[0]].copy()
        added.loc[:, ["atom1_index", "atom2_index"]] = [
            extra,
            int(options["selection"][0]),
        ]
        state.bonds = pd.concat([state.bonds, added], ignore_index=True)
    else:
        options["connectivity_policy"] = "complete_from_template"
    before = source.copy()
    assessment = msm.physchem.assess_chemical_template(source, **options)
    assert assessment["status"] == (
        "unassessed" if failure in {"missing_context", "completion"} else "conflict"
    )
    assert assessment["issues"]
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **options)
    assert_tree(error.value.report, assessment)
    pd.testing.assert_frame_equal(
        state.atom_attributes, before.chemical_states._states[0].atom_attributes
    )
    pd.testing.assert_frame_equal(state.bonds, before.chemical_states._states[0].bonds)
    assert_tree(
        source.chemical_states.get_preparation_history(),
        before.chemical_states.get_preparation_history(),
    )
    assert source.interactions["old"].evaluated_structure_indices.tolist() == [0, 1]


@pytest.mark.parametrize(
    "invalid",
    ["overlap", "duplicate", "out_of_range", "float", "bool", "shape", "empty_list"],
)
def test_context_maps_must_be_disjoint_typed_bijections(invalid):
    source, options = peptide_case()
    history = source.chemical_states.get_preparation_history()
    context = options["context_atom_correspondence"].copy()
    if invalid == "overlap":
        context[0] = options["atom_correspondence"][0]
    elif invalid == "duplicate":
        context[0] = context[1]
    elif invalid == "out_of_range":
        context[0, 0] = source.get_n_atoms()
    elif invalid == "float":
        context = context.astype(float)
    elif invalid == "bool":
        context = context.astype(bool)
    elif invalid == "shape":
        context = context[:, 0]
    else:
        context = []
    options["context_atom_correspondence"] = context
    with pytest.raises(ArgumentError):
        msm.physchem.apply_chemical_template(source, **options)
    assert_tree(source.chemical_states.get_preparation_history(), history)


def test_incident_stereo_bond_requires_context_references():
    template = _stereo_template()
    source = _source(template)
    source.chemical_states._states[0].bonds.drop(
        columns=["stereochemistry", "stereo_atom1_index", "stereo_atom2_index"],
        inplace=True,
    )
    options = dict(
        template=template,
        template_provenance=dict(PROVENANCE, hydrogen_policy="stored_counts"),
        selection=[1],
        atom_correspondence=[[1, 1]],
        context_atom_correspondence=[[0, 0], [2, 2]],
    )
    assessment = msm.physchem.assess_chemical_template(source, **options)
    assert assessment["status"] == "unassessed"
    assert "unmapped_template_stereo_context" in {
        i["reason_code"] for i in assessment["issues"]
    }
    options["context_atom_correspondence"].append([3, 3])
    output = msm.physchem.apply_chemical_template(source, **options)["molecular_system"]
    bond = output.chemical_states.get_bonds().iloc[1]
    assert bond.stereochemistry == "E"
    assert (bond.stereo_atom1_index, bond.stereo_atom2_index) == (0, 3)


def test_disulfide_link_is_covered_without_assigning_external_cysteine():
    source, options = peptide_case(
        ["CYX", "GLY", "CYX"], disulfide_group_pairs=[[0, 2]]
    )
    definition = msm.physchem.get_peptide_chemical_template(
        ["CYX", "GLY", "CYX"], "ammonium", "carboxylate", disulfide_group_pairs=[[0, 2]]
    )
    selected = msm.select(source, selection="group_index == 0")
    pairs = source.chemical_states.get_bonds()[["atom1_index", "atom2_index"]].to_numpy(
        dtype=np.int64
    )
    context = np.setdiff1d(pairs[np.isin(pairs, selected).any(axis=1)], selected)
    options.update(
        template=definition["template"],
        template_provenance=definition["template_provenance"],
        selection=selected,
        atom_correspondence=np.column_stack((selected, selected)),
        context_atom_correspondence=np.column_stack((context, context)),
    )
    output = msm.physchem.apply_chemical_template(source, **options)
    result = output["molecular_system"]
    sulfurs = result.topology.atoms.index[
        result.topology.atoms.atom_name == "SG"
    ].to_numpy()
    sulfur_bond = result.chemical_states.get_bonds()
    sulfur_bond = sulfur_bond[
        np.isin(sulfur_bond[["atom1_index", "atom2_index"]], sulfurs).all(axis=1)
    ]
    assert sulfur_bond.bond_order.tolist() == [1]
    assert (
        result.chemical_states._states[0].atom_attributes.at[
            int(sulfurs[0]), "n_explicit_hydrogens"
        ]
        == 0
    )
    assert pd.isna(
        result.chemical_states._states[0].atom_attributes.at[
            int(sulfurs[1]), "formal_charge"
        ]
    )
    assert result.chemical_states._states[0].connectivity_completeness == "partial"


@pytest.mark.parametrize("references", [[0, 0], [1, 3], [0, 99]])
def test_invalid_source_stereo_is_rejected_in_context_mode(references):
    template = _stereo_template()
    source = _source(template)
    bonds = source.chemical_states.get_bonds()
    bonds.loc[1, "stereochemistry"] = "E"
    bonds.loc[1, ["stereo_atom1_index", "stereo_atom2_index"]] = references
    before = bonds.copy(deep=True)
    options = dict(
        template=template,
        template_provenance=dict(PROVENANCE, hydrogen_policy="stored_counts"),
        selection=[1],
        atom_correspondence=[[1, 1]],
        context_atom_correspondence=[[0, 0], [2, 2], [3, 3]],
    )
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **options)
    assert "invalid_stereo_reference_atoms" in {
        item["reason_code"] for item in error.value.report["issues"]
    }
    pd.testing.assert_frame_equal(bonds, before)


def test_disconnected_selection_and_repetition_preserve_explicit_coverage():
    source, options = peptide_case()
    history = source.chemical_states.get_preparation_history()
    selected = msm.select(source, selection="group_index in [0, 2]")
    context = np.setdiff1d(np.arange(source.get_n_atoms()), selected)
    options.update(
        selection=np.r_[selected[::-1], selected[0]],
        atom_correspondence=np.column_stack((selected, selected)),
        context_atom_correspondence=np.column_stack((context, context)),
    )
    output = msm.physchem.apply_chemical_template(source, **options)["molecular_system"]
    assert output.chemical_states._states[0].connectivity_completeness == "partial"
    output.interactions = {
        "fresh": msm.Interactions.from_records(
            [],
            n_atoms=output.get_n_atoms(),
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="control",
        )
    }
    repeated = msm.physchem.apply_chemical_template(output, **options)
    assert repeated["report"]["assigned_fields"] == []
    assert repeated["report"]["invalidated_analysis_names"] == []
    assert repeated["molecular_system"].interactions[
        "fresh"
    ].evaluated_structure_indices.tolist() == [0, 1]
    retained = repeated["molecular_system"].chemical_states.get_preparation_history()
    assert len(retained) == len(history) + 2
    assert_tree(retained[:-2], history)


def test_empty_context_assignment_scope_does_not_certify_preparation():
    source, options = peptide_case()
    history = source.chemical_states.get_preparation_history()
    options.update(selection=[], atom_correspondence=np.empty((0, 2), dtype=np.int64))
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **options)
    assert error.value.report["status"] == "unassessed"
    assert error.value.report["issues"][0]["reason_code"] == "empty_assignment_scope"
    assert_tree(source.chemical_states.get_preparation_history(), history)


@pytest.fixture(scope="module")
def observed_polymer_context(est_case):
    _, manifest = est_case  # Verifies the pinned deposited bytes and source axes.
    full = msm.convert(DATA / "1qku.cif.gz", to_form="molsysmt.MolSys")
    receptor_selection = 'molecule_type == "protein" and chain_id == "A"'
    indices = msm.select(full, selection=receptor_selection)
    receptor = msm.extract(full, selection=indices)
    assert receptor.get_n_atoms() == 1990
    assert len(receptor.topology.groups) == 250
    names = receptor.topology.groups.group_name.tolist()
    definition = msm.physchem.get_peptide_chemical_template(
        ["HIE" if name == "HIS" else name for name in names], "ammonium", "carboxylate"
    )
    lookup = {
        (int(row.group_index), row.atom_name): int(index)
        for index, row in receptor.topology.atoms.iterrows()
    }
    mapping, missing = [], []
    for index, row in definition["template"].topology.atoms.iterrows():
        name = row.atom_name
        if names[int(row.group_index)] == "ARG" and name in {"NH1", "NH2"}:
            name = "NH2" if name == "NH1" else "NH1"
        source_index = lookup.get((int(row.group_index), name))
        if source_index is None:
            missing.append(int(index))
        else:
            mapping.append((int(index), source_index))
    mapping = np.asarray(mapping, dtype=np.int64)
    assert sorted(mapping[:, 1].tolist()) == list(range(1990))
    assert len(missing) == 9
    # The separate explicit representation operation records changes across the receptor.
    normalized = msm.physchem.normalize_aromatic_bond_orders(receptor)[
        "molecular_system"
    ]
    shells = {}
    for distance, count in [(0.4, 12), (0.5, 19), (0.6, 23)]:
        full_groups = msm.select(
            full,
            selection=f"({receptor_selection}) within {distance} nm without pbc of ({manifest['source_selection']})",
            element="group",
        )
        ids = full.topology.groups.group_id.iloc[full_groups].tolist()
        assert len(ids) == count
        groups = receptor.topology.groups.index[
            receptor.topology.groups.group_id.isin(ids)
        ].to_numpy()
        selected = msm.select(receptor, selection=f"group_index in {groups.tolist()}")
        shells[distance] = (selected, groups)
    return full, receptor, normalized, definition, mapping, np.asarray(missing), shells


@pytest.mark.parametrize(
    "distance,form", [(0.4, "native"), (0.5, "native"), (0.6, "native"), (0.5, "h5msm")]
)
def test_observed_1qku_shell_keeps_full_chain_context_and_unassessed_gaps(
    observed_polymer_context, tmp_path, distance, form
):
    full, original, source, definition, mapping, missing, shells = (
        observed_polymer_context
    )
    source_history = source.chemical_states.get_preparation_history()
    selected, groups = shells[distance]
    assignment_map = mapping[np.isin(mapping[:, 1], selected)]
    context_map = mapping[~np.isin(mapping[:, 1], selected)]
    options = dict(
        template=definition["template"],
        template_provenance=definition["template_provenance"],
        selection=selected,
        atom_correspondence=assignment_map,
        context_atom_correspondence=context_map,
    )
    molecular_system = source
    if form == "h5msm":
        molecular_system = tmp_path / "receptor.h5msm"
        msm.convert(source, to_form=molecular_system)
    result = msm.physchem.apply_chemical_template(molecular_system, **options)
    output, report = result["molecular_system"], result["report"]
    assert report["status"] == "applied", report["issues"]
    assert report["coverage"]["scope"] == "selected_with_context"
    assert report["coverage"]["graph"] == "same_stored_relationships"
    np.testing.assert_array_equal(
        report["coverage"]["unmapped_template_atom_indices"], missing
    )
    assert output.chemical_states._states[0].connectivity_completeness == "partial"
    assert report["added_bonds"] == []
    assert set(original.topology.groups.group_id.iloc[groups]).isdisjoint(
        {"301", "302", "303"}
    )
    fields = msm.physchem.get_chemical_readiness(output, selection=selected)["fields"]
    for field in (
        "formal_charge",
        "atom_is_aromatic",
        "n_unpaired_electrons",
        "n_explicit_hydrogens",
        "n_implicit_hydrogens",
    ):
        assert fields[field]["status"] == "present", (field, fields[field]["status"])
    outside = np.setdiff1d(np.arange(1990), selected)
    original_fields = source.chemical_states._states[0].atom_attributes.columns
    if len(original_fields):
        pd.testing.assert_frame_equal(
            output.chemical_states._states[0].atom_attributes.iloc[outside][
                original_fields
            ],
            source.chemical_states._states[0].atom_attributes.iloc[outside],
        )
    assert (
        output.chemical_states._states[0]
        .atom_attributes.iloc[outside]
        .isna()
        .all()
        .all()
    )
    before_bonds = source.chemical_states.get_bonds()
    pairs = before_bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    outside_bonds = ~np.isin(pairs, selected).any(axis=1)
    pd.testing.assert_frame_equal(
        output.chemical_states.get_bonds()[outside_bonds][before_bonds.columns],
        before_bonds[outside_bonds],
        check_dtype=False,
        check_like=True,
    )
    new_bond_fields = output.chemical_states.get_bonds().columns.difference(
        before_bonds.columns
    )
    assert (
        output.chemical_states.get_bonds()
        .loc[outside_bonds, new_bond_fields]
        .isna()
        .all()
        .all()
    )
    np.testing.assert_array_equal(
        report["coverage"]["external_source_bond_indices"],
        np.flatnonzero(np.isin(pairs, selected).sum(axis=1) == 1),
    )
    assert len(report["coverage"]["external_source_bond_indices"]) > 0
    pd.testing.assert_frame_equal(output.topology.atoms, original.topology.atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(original.structures.coordinates, to_unit="nm"),
    )
    assert_tree(
        source.chemical_states.get_preparation_history(),
        source_history,
    )
    assert original.chemical_states.get_preparation_history() == ()
    assert full.chemical_states._states[0].atom_attributes.empty
    path = tmp_path / "prepared-shell.h5msm"
    msm.convert(output, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert_tree(
        loaded.chemical_states.get_preparation_history(),
        output.chemical_states.get_preparation_history(),
    )
    # Declared scoped preparation cannot justify recognition of the whole receptor.
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_hbond_sites(loaded, method="smarts_donor_acceptor")


def test_cookbook_polymer_context_block_executes_on_the_observed_control(
    observed_polymer_context, tmp_path, monkeypatch
):
    full, receptor, _, _, _, _, _ = observed_polymer_context
    page = (
        Path(__file__).resolve().parents[2]
        / "docs/content/user/cookbook/applying_chemical_templates.md"
    )
    section = (
        page.read_text()
        .split("(cookbook-polymer-context-template)=", 1)[1]
        .split("## Assessing excluded residue gaps", 1)[0]
    )
    blocks = re.findall(r"```python\n(.*?)```", section, re.S)
    assert len(blocks) == 1
    namespace = dict(msm=msm, molsys=full)
    monkeypatch.chdir(tmp_path)
    exec(compile(blocks[0], str(page), "exec"), namespace)
    loaded = msm.convert(
        tmp_path / "receptor_with_prepared_shell.h5msm", to_form="molsysmt.MolSys"
    )
    assert loaded.get_n_atoms() == 1990
    assert loaded.chemical_states._states[0].connectivity_completeness == "partial"
    history = loaded.chemical_states.get_preparation_history()
    assert [item["report"]["schema"] for item in history] == [
        "molsysmt.aromatic_bond_normalization@1",
        "molsysmt.chemical_template@1",
        "molsysmt.peptide_template@1",
    ]
    assert [item["output"]["n_atoms"] for item in history] == [1990, 1990, 1999]
    assert_tree(
        loaded.chemical_states.get_preparation_history(),
        namespace["molsys_B"].chemical_states.get_preparation_history(),
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(receptor.structures.coordinates, to_unit="nm"),
    )
    assert full.chemical_states._states[0].atom_attributes.empty
