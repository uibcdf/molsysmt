"""Independent candidates and coordinated in-place molecular removal."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys
from molsysmt.native.h5msm_file_handler import H5MSMFileHandler


@pytest.fixture
def observed_system():
    molsys = MolSys(n_atoms=4)
    molsys.topology.atoms["atom_id"] = ["10", "20", "30", "40"]
    molsys.topology.atoms["atom_name"] = ["N", "O", "C", "S"]
    molsys.topology.atoms["atom_type"] = ["N", "O", "C", "S"]
    molsys.topology._set_chemical_state_atom_attribute("formal_charge", [0, -1, 0, 1])
    molsys.topology._append_chemical_state_bonds([[0, 1], [2, 3]], orders=1)
    molsys.structures.coordinates = msm.pyunitwizard.quantity(
        np.arange(48, dtype=float).reshape(4, 4, 3), "angstrom"
    )
    molsys.structures.box = msm.pyunitwizard.quantity(
        np.tile(np.eye(3) * 50, (4, 1, 1)), "angstrom"
    )
    molsys.structures.time = msm.pyunitwizard.quantity(np.arange(4.0), "ps")
    molsys.structures.structure_id = np.array(["a", "b", "c", "d"])
    molsys.molecular_mechanics.atoms_ff = pd.DataFrame(
        {"partial_charge": [0.1, -0.1, 0.2, -0.2]}
    )
    molsys.topology._append_chemical_state(state_id="second")
    molsys.topology._set_reference_chemical_state_index(0)
    molsys._set_structure_chemical_state_indices([0, 1, 0, 1])
    records = [
        {
            "structure_index": structure,
            "interaction_type": "pair",
            "participants": [
                {"role": "first", "atom_indices": [first]},
                {"role": "second", "atom_indices": [second]},
            ],
        }
        for structure, first, second in [(0, 0, 1), (0, 0, 1), (2, 0, 1), (2, 2, 3)]
    ]
    result = msm.Interactions.from_records(
        records,
        n_atoms=4,
        n_structures=4,
        evaluated_structure_indices=[0, 1, 2],
        method="declared-pairs",
        source_id="original-system",
    )
    molsys.interactions = {"pairs": result, "other": result.copy()}
    return molsys


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "selection,structures,atoms_kept,structures_kept",
    [
        ([2], None, [0, 1, 3], [0, 1, 2, 3]),
        (None, [1, 3, 1], [0, 1, 2, 3], [0, 2]),
        ([2], [1, 3], [0, 1, 3], [0, 2]),
        ([], [], [0, 1, 2, 3], [0, 1, 2, 3]),
        (None, None, [0, 1, 2, 3], [0, 1, 2, 3]),
        ("all", None, [], [0, 1, 2, 3]),
        (None, "all", [0, 1, 2, 3], []),
        ("all", "all", [], []),
    ],
)
def test_modes_preserve_axes_values_and_original_snapshots(
    observed_system, in_place, selection, structures, atoms_kept, structures_kept
):
    source = observed_system
    original_topology = source.topology
    original_structures = source.structures
    original_chemistry = source.chemical_states
    analyses = dict(source.interactions)
    original_view = analyses["pairs"].query(structure_indices=[0])
    original_coordinates = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="angstrom"
    ).copy()

    returned = msm.remove(
        source, selection=selection, structure_indices=structures, in_place=in_place
    )
    result = source if in_place else returned
    assert returned is None if in_place else result is not source
    assert result.topology.n_atoms == len(atoms_kept)
    assert result.structures.n_structures == len(structures_kept)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="angstrom"),
        original_coordinates[np.ix_(structures_kept, atoms_kept, [0, 1, 2])],
    )
    np.testing.assert_array_equal(
        result.structures.structure_id, np.array(["a", "b", "c", "d"])[structures_kept]
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.time, to_unit="ps"),
        np.arange(4.0)[structures_kept],
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.box, to_unit="angstrom"),
        np.tile(np.eye(3) * 50, (len(structures_kept), 1, 1)),
    )
    assert result.topology.atoms["atom_id"].tolist() == [
        ["10", "20", "30", "40"][i] for i in atoms_kept
    ]
    np.testing.assert_allclose(
        result.molecular_mechanics.atoms_ff["partial_charge"],
        np.array([0.1, -0.1, 0.2, -0.2])[atoms_kept],
    )
    assert result.topology._chemical_states_domain is result.chemical_states
    assert result.topology._molsys_owner_ref() is result
    assert result.structures._molsys_owner_ref() is result
    assert result.chemical_states._molsys_owner_ref() is result
    assert result._structure_chemical_state_indices.tolist() == [
        [0, 1, 0, 1][i] for i in structures_kept
    ]

    expected_evaluated = [
        new for new, old in enumerate(structures_kept) if old in (0, 1, 2)
    ]
    for name, analysis in result.interactions.items():
        assert (analysis.n_atoms, analysis.n_structures) == (
            len(atoms_kept),
            len(structures_kept),
        )
        assert analysis.source_id == "original-system"
        np.testing.assert_array_equal(analysis.atom_source_indices, atoms_kept)
        np.testing.assert_array_equal(
            analysis.structure_source_indices, structures_kept
        )
        np.testing.assert_array_equal(
            analysis.evaluated_structure_indices, expected_evaluated
        )
        expected_occurrences = sum(
            structure in structures_kept
            and first in atoms_kept
            and second in atoms_kept
            for structure, first, second in [(0, 0, 1), (0, 0, 1), (2, 0, 1), (2, 2, 3)]
        )
        assert analysis.n_interactions == expected_occurrences
        assert analyses[name].n_interactions == 4
    assert original_view.n_interactions == 2
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(original_structures.coordinates, to_unit="angstrom"),
        original_coordinates,
    )
    assert original_topology.n_atoms == original_chemistry.n_atoms == 4
    if not in_place:
        assert source.topology is original_topology
        assert source.structures is original_structures
        assert source.chemical_states is original_chemistry


@pytest.mark.parametrize("kwargs", [{}, {"selection": []}, {"structure_indices": []}])
def test_default_and_empty_removal_return_independent_candidates(
    observed_system, kwargs
):
    source = observed_system
    result = msm.remove(source, **kwargs)
    assert result is not source
    assert result.topology is not source.topology
    assert result.structures is not source.structures
    assert result.chemical_states is not source.chemical_states
    result.topology.atoms.loc[0, "atom_name"] = "changed"
    assert source.topology.atoms.loc[0, "atom_name"] == "N"
    result.structures.set_coordinates(
        value=msm.pyunitwizard.quantity([[[99.0, 0, 0]]], "angstrom"),
        indices=[0],
        structure_indices=[0],
    )
    assert result.interactions["pairs"].query(structure_indices=[0]).n_interactions == 0
    assert source.interactions["pairs"].query(structure_indices=[0]).n_interactions == 2


def test_in_place_rebinds_new_domains_and_detaches_retained_old_domains(
    observed_system,
):
    source = observed_system
    old_domains = source.topology, source.structures, source.chemical_states
    msm.remove(source, selection=[2], in_place=True)
    for old in old_domains:
        owner = getattr(old, "_molsys_owner_ref", None)
        assert owner is None or owner() is None
    old_domains[1].set_coordinates(
        value=msm.pyunitwizard.quantity([[[99.0, 0, 0]]], "nm"),
        indices=[0],
        structure_indices=[0],
    )
    assert source.interactions["pairs"].query(structure_indices=[0]).n_interactions == 2
    source.structures.set_coordinates(
        value=msm.pyunitwizard.quantity([[[99.0, 0, 0]]], "nm"),
        indices=[0],
        structure_indices=[0],
    )
    assert source.interactions["pairs"].query(structure_indices=[0]).n_interactions == 0


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "kwargs", [{"selection": [4]}, {"selection": [-1]}, {"structure_indices": [4]}]
)
def test_invalid_request_preserves_source(observed_system, in_place, kwargs):
    source = observed_system
    old_domains = source.topology, source.structures, source.chemical_states
    old_analysis = source.interactions["pairs"]
    with pytest.raises(ArgumentError):
        msm.remove(source, in_place=in_place, **kwargs)
    assert (source.topology, source.structures, source.chemical_states) == old_domains
    assert source.interactions["pairs"] is old_analysis
    assert source.topology.n_atoms == 4
    assert source.structures.n_structures == 4


@pytest.mark.parametrize("in_place", [False, True])
def test_remapping_failure_does_not_publish_candidate(
    observed_system, monkeypatch, in_place
):
    source = observed_system
    old_domains = source.topology, source.structures, source.chemical_states
    old_analysis = source.interactions["pairs"]

    def fail(*args, **kwargs):
        raise MemoryError("cannot allocate remapped observations")

    monkeypatch.setattr(msm.Interactions, "remap", fail)
    with pytest.raises(MemoryError, match="remapped observations"):
        msm.remove(source, selection=[2], in_place=in_place)
    assert (source.topology, source.structures, source.chemical_states) == old_domains
    assert source.interactions["pairs"] is old_analysis
    assert source.topology._molsys_owner_ref() is source


@pytest.mark.parametrize("domain", ["topology", "structures"])
def test_in_place_attached_domain_is_rejected(observed_system, domain):
    with pytest.raises(ArgumentError, match="attached"):
        msm.remove(getattr(observed_system, domain), selection=[0], in_place=True)
    assert observed_system.topology.n_atoms == 4
    assert observed_system.structures.n_atoms == 4


@pytest.mark.parametrize("domain", ["topology", "structures"])
@pytest.mark.parametrize("in_place", [False, True])
def test_standalone_native_domain_removal(observed_system, domain, in_place):
    source = getattr(observed_system, domain).copy()
    returned = msm.remove(source, selection=[2], in_place=in_place)
    result = source if in_place else returned
    assert returned is None if in_place else result is not source
    assert result.n_atoms == 3
    assert observed_system.topology.n_atoms == observed_system.structures.n_atoms == 4


def test_in_place_rejects_conversion_and_complementary_input(observed_system):
    with pytest.raises(ArgumentError, match="to_form"):
        msm.remove(
            observed_system, selection=[2], to_form="molsysmt.Topology", in_place=True
        )
    with pytest.raises(ArgumentError, match="in_place"):
        msm.remove(
            [observed_system.topology, observed_system.structures],
            selection=[2],
            in_place=True,
        )
    assert observed_system.topology.n_atoms == 4


@pytest.mark.parametrize("in_place", [False, True])
def test_h5msm_input_requires_explicit_out_of_place_mode(
    observed_system, tmp_path, in_place
):
    path = tmp_path / "original.h5msm"
    observed_system.molecular_mechanics.atoms_ff = None
    msm.convert(observed_system, to_form="file:h5msm", output_filename=path)
    original_bytes = path.read_bytes()
    if in_place:
        with pytest.raises(ArgumentError, match="in_place"):
            msm.remove(path, selection=[2], in_place=True)
    else:
        result = msm.remove(
            path, selection=[2], to_form="molsysmt.MolSys", in_place=False
        )
        assert result.topology.n_atoms == 3
        assert result.interactions["pairs"].n_interactions == 3
    assert path.read_bytes() == original_bytes


@pytest.mark.parametrize("in_place", [False, True])
def test_projected_analyses_survive_h5msm_round_trip(
    observed_system, tmp_path, in_place
):
    source = observed_system
    returned = msm.remove(
        source, selection=[2], structure_indices=[3], in_place=in_place
    )
    result = source if in_place else returned
    result.molecular_mechanics.atoms_ff = None
    path = tmp_path / "trimmed.h5msm"
    msm.convert(result, to_form="file:h5msm", output_filename=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert restored.topology._chemical_states_domain is restored.chemical_states
    assert restored._structure_chemical_state_indices.tolist() == [0, 1, 0]
    for analysis in restored.interactions.values():
        np.testing.assert_array_equal(analysis.atom_source_indices, [0, 1, 3])
        np.testing.assert_array_equal(analysis.structure_source_indices, [0, 1, 2])
        payload = analysis.query(structure_indices=[2, 0, 1]).to_dict()
        np.testing.assert_array_equal(payload["evaluated_structure_indices"], [2, 0, 1])
        assert len(np.unique(payload["occurrence_indices"])) == 3
        assert analysis.query(structure_indices=[1]).n_interactions == 0
        assert analysis.query(structure_indices=[0]).n_interactions == 2


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("domains", ["structures", "topology", "interactions"])
def test_partial_molsys_remaps_declared_axes(observed_system, domains, in_place):
    topology = observed_system.topology.copy() if domains == "topology" else None
    source = MolSys._from_partial_domains(
        topology=topology,
        chemical_states=None if topology is None else topology._chemical_states_domain,
        structures=observed_system.structures.copy()
        if domains == "structures"
        else None,
        interactions=dict(observed_system.interactions),
    )
    returned = msm.remove(
        source, selection=[2], structure_indices=[3], in_place=in_place
    )
    result = source if in_place else returned
    assert (result.topology is None) == (domains != "topology")
    assert (result.structures is None) == (domains != "structures")
    assert result.interactions["pairs"].n_atoms == 3
    assert result.interactions["pairs"].n_structures == 3
    assert result.interactions["pairs"].n_interactions == 3


@pytest.mark.parametrize("form", ["molsysmt.MolSysDict", "complementary"])
def test_other_forms_keep_independent_out_of_place_route(observed_system, form):
    observed_system.molecular_mechanics.atoms_ff = None
    observed_system.interactions = {}
    if form == "molsysmt.MolSysDict":
        # The documented 0.1 builder route reads structure labels as integers.
        observed_system.structures.structure_id = np.array([10, 20, 30, 40])
    source = (
        [observed_system.topology, observed_system.structures]
        if form == "complementary"
        else msm.convert(observed_system, to_form=form)
    )
    result = msm.remove(source, selection=[2], to_form="molsysmt.MolSys")
    assert result.topology.n_atoms == 3
    assert observed_system.topology.n_atoms == 4
    result.topology.atoms.loc[0, "atom_name"] = "edited"
    assert observed_system.topology.atoms.loc[0, "atom_name"] == "N"


def test_noop_in_place_keeps_domains_and_extension_state(observed_system):
    source = observed_system
    metadata = {"self": source}
    source.client_metadata = metadata
    old_domains = source.topology, source.structures, source.chemical_states
    analysis = source.interactions["pairs"]
    assert msm.remove(source, selection=[], structure_indices=[], in_place=True) is None
    assert (source.topology, source.structures, source.chemical_states) == old_domains
    assert source.interactions["pairs"] is analysis
    msm.remove(source, selection=[2, 2], in_place=True)
    assert source.client_metadata is metadata
    assert source.client_metadata["self"] is source
    assert source.topology.n_atoms == 3


def test_nested_in_place_removal_is_rejected_before_publication(observed_system):
    source = observed_system
    with source._invalidating_interaction_frames([0]):
        with pytest.raises(ArgumentError, match="active molecular edit"):
            msm.remove(source, selection=[2], in_place=True)
    assert source.topology.n_atoms == 4
    assert source.structures.n_atoms == 4


@pytest.mark.parametrize("value", [1, None, "true"])
def test_non_boolean_mutation_flag_is_rejected(observed_system, value):
    source = observed_system
    with pytest.raises(ArgumentError):
        msm.remove(source, selection=[2], in_place=value)
    assert source.topology.n_atoms == source.structures.n_atoms == 4


@pytest.mark.parametrize("selection", [None, [2]])
@pytest.mark.parametrize("target", [None, "form", "source", "hardlink", "handler"])
def test_file_removal_rejects_aliased_or_implicit_destination(
    observed_system, tmp_path, target, selection
):
    source = observed_system
    source.molecular_mechanics.atoms_ff = None
    path = tmp_path / "source.h5msm"
    msm.convert(source, to_form=path)
    original = path.read_bytes()
    destination = {
        None: None,
        "form": "file:h5msm",
        "source": path,
        "hardlink": tmp_path / "alias.h5msm",
        "handler": "molsysmt.H5MSMFileHandler",
    }[target]
    if target == "hardlink":
        destination.hardlink_to(path)
    with pytest.raises(ArgumentError, match="to_form"):
        msm.remove(path, selection=selection, to_form=destination)
    assert path.read_bytes() == original


@pytest.mark.parametrize("selection", [None, [2]])
def test_distinct_file_output_is_independent(observed_system, tmp_path, selection):
    observed_system.molecular_mechanics.atoms_ff = None
    source = tmp_path / "source.h5msm"
    destination = tmp_path / "trimmed.h5msm"
    msm.convert(observed_system, to_form=source)
    original = source.read_bytes()
    msm.remove(source, selection=selection, to_form=destination)
    result = msm.convert(destination, to_form="molsysmt.MolSys")
    assert result.topology.n_atoms == (4 if selection is None else 3)
    assert source.read_bytes() == original


def test_file_handler_requires_explicit_independent_output(tmp_path):
    from shutil import copyfile

    path = tmp_path / "source.h5msm"
    copyfile(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"], path)
    # Native file handlers currently read legacy schemas, not H5MSM 0.5.
    handler = H5MSMFileHandler(path)
    try:
        with pytest.raises(ArgumentError, match="to_form"):
            msm.remove(handler)
        with pytest.raises(ArgumentError, match="to_form"):
            msm.remove(handler, to_form=path)
        result = msm.remove(handler, selection=[2], to_form="molsysmt.MolSys")
        assert result.topology.n_atoms == 21
        assert handler.file.id.valid
    finally:
        handler.close()
