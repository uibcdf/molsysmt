"""Graph endpoints, source axes and explicit ambiguity refusals."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


def _atom(molsys, group, name):
    return int(
        molsys.topology.atoms[
            (molsys.topology.atoms["group_index"] == group)
            & (molsys.topology.atoms["atom_name"] == name)
        ].index[0]
    )


def _peptide():
    return msm.build.build_peptide("AlaValPro", engine="MolSysMT")


def test_free_ends_and_sparse_source_index_arrays():
    molsys = _peptide()
    report = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(report["n_terminal_group_indices"], [0])
    np.testing.assert_array_equal(report["c_terminal_group_indices"], [2])
    np.testing.assert_array_equal(report["chains"][0]["group_indices"], [0, 1, 2])
    assert report["method"] == "stored_backbone_connectivity"
    assert (
        report["chemical_state_index"]
        == molsys.chemical_states.reference_chemical_state_index
    )
    for key in [
        "n_terminal_group_indices",
        "c_terminal_group_indices",
        "n_capped_group_indices",
        "c_capped_group_indices",
    ]:
        assert report[key].dtype == np.dtype("int64")
        assert report[key].ndim == 1


@pytest.mark.parametrize(
    "selection", [[], "group_index==1", "atom_name=='CA' and group_index==1"]
)
def test_selection_does_not_create_endpoints(selection):
    report = msm.chemical_states.get_peptide_termini(_peptide(), selection=selection)
    assert report["n_terminal_group_indices"].shape == (0,)
    assert report["c_terminal_group_indices"].shape == (0,)


def test_attached_caps_are_bonds_not_labels_or_inventory_positions():
    molsys = msm.build.build_peptide("AceAlaValProNme", engine="MolSysMT")
    msm.set(molsys, element="group", group_id=["z", "d", "c", "b", "a"])
    report = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(report["n_capped_group_indices"], [1])
    np.testing.assert_array_equal(report["c_capped_group_indices"], [3])
    assert not len(report["n_terminal_group_indices"])
    assert not len(report["c_terminal_group_indices"])


def test_cap_like_id_labels_do_not_mask_a_free_terminus():
    molsys = _peptide()
    # Naming an amino acid like a cap would change chemistry interpretation;
    # ID labels alone never do so.
    msm.set(molsys, element="group", group_id=["ACE", "NME", "NME"])
    report = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(report["c_terminal_group_indices"], [2])


def test_a_cycle_has_no_free_ends_and_does_not_acquire_caps():
    molsys = _peptide()
    molsys.chemical_states.add_bonds([[_atom(molsys, 2, "C"), _atom(molsys, 0, "N")]])
    report = msm.chemical_states.get_peptide_termini(molsys)
    assert report["chains"][0]["cyclic"]
    assert report["chains"][0]["n_terminal_group_index"] is None
    assert not len(report["n_terminal_group_indices"])
    assert not len(report["c_terminal_group_indices"])
    before = molsys.copy()
    with pytest.raises(
        msm.StructuralInconsistencyError, match="linear named peptide backbone"
    ):
        msm.build.add_missing_terminal_cappings(molsys, N_terminal="ACE")
    assert molsys.chemical_states._inventory_equals(before.chemical_states)


def test_missing_link_is_ambiguous_not_two_fabricated_termini():
    molsys = _peptide()
    pair = {_atom(molsys, 0, "C"), _atom(molsys, 1, "N")}
    bonds = molsys.chemical_states.get_bonds()
    index = next(
        i
        for i, row in bonds.iterrows()
        if {int(row["atom1_index"]), int(row["atom2_index"])} == pair
    )
    molsys.chemical_states.remove_bonds([int(index)])
    with pytest.raises(msm.StructuralInconsistencyError, match="Disconnected"):
        msm.chemical_states.get_peptide_termini(molsys)


def test_branch_is_refused_instead_of_picking_a_group_id():
    molsys = _peptide()
    molsys.chemical_states.add_bonds([[_atom(molsys, 0, "C"), _atom(molsys, 2, "N")]])
    with pytest.raises(msm.StructuralInconsistencyError, match="Branched"):
        msm.chemical_states.get_peptide_termini(molsys)


def test_atom_permutation_preserves_group_endpoints_and_source_data():
    molsys = _peptide()
    permutation = np.arange(molsys.get(n_atoms=True))[::-1]
    other = msm.permute_atoms(molsys, permutation)
    before = other.copy()
    report = msm.chemical_states.get_peptide_termini(other)
    np.testing.assert_array_equal(report["n_terminal_group_indices"], [0])
    np.testing.assert_array_equal(report["c_terminal_group_indices"], [2])
    assert other.chemical_states._inventory_equals(before.chemical_states)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(other.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(before.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize("form", ["molsysmt.MolSysDict", "mdtraj.Trajectory"])
def test_supported_forms_retain_source_group_indices(form):
    molsys = _peptide()
    molsys.molecular_mechanics = None
    source = msm.convert(molsys, to_form=form)
    report = msm.chemical_states.get_peptide_termini(source)
    np.testing.assert_array_equal(report["n_terminal_group_indices"], [0])
    np.testing.assert_array_equal(report["c_terminal_group_indices"], [2])


def test_topology_alone_has_no_chemical_endpoint_authority():
    with pytest.raises(msm.StructuralInconsistencyError, match="stored chemical"):
        msm.chemical_states.get_peptide_termini(_peptide().topology)


def test_no_coordinate_values_are_needed_for_recognition():
    molsys = _peptide()
    molsys.structures = None
    report = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(report["c_terminal_group_indices"], [2])


def test_explicit_state_and_structure_association_do_not_change_reference():
    molsys = _peptide()
    pairs = molsys.chemical_states.get_bonds()[["atom1_index", "atom2_index"]].to_numpy(
        dtype=int
    )
    state = molsys.chemical_states.append_state()
    molsys.chemical_states.add_bonds(pairs, chemical_state=state)
    molsys.chemical_states.add_bonds(
        [[_atom(molsys, 2, "C"), _atom(molsys, 0, "N")]], chemical_state=state
    )
    reference = molsys.chemical_states.reference_chemical_state_index
    report = msm.chemical_states.get_peptide_termini(molsys, chemical_state=state)
    assert report["chemical_state_index"] == state
    assert report["chains"][0]["cyclic"]
    msm.set(molsys, structure_chemical_state_index=[state])
    associated = msm.chemical_states.get_peptide_termini(
        molsys, chemical_state="structure", structure_indices=[0]
    )
    assert associated["chains"][0]["cyclic"]
    assert molsys.chemical_states.reference_chemical_state_index == reference
    assert msm.chemical_states.get_peptide_termini(molsys)[
        "c_terminal_group_indices"
    ].tolist() == [2]


def _reorder_groups(molsys, order):
    builder = msm.MolSysBuilder()
    old_to_new = {}
    source_order = []
    for old_group in order:
        indices = []
        for old, row in molsys.topology.atoms[
            molsys.topology.atoms["group_index"] == old_group
        ].iterrows():
            new = builder.add_atom(
                atom_id=row["atom_id"],
                atom_name=row["atom_name"],
                atom_type=row["atom_type"],
            )
            indices.append(new)
            source_order.append(old)
            old_to_new[old] = new
        builder.add_group(
            indices,
            group_name=molsys.topology.groups.loc[old_group, "group_name"],
            group_id=f"source-{old_group}",
        )
    builder.add_chain([order.index(g) for g in range(len(order))], chain_id="A")
    for _, row in molsys.chemical_states.get_bonds().iterrows():
        builder.add_bond(
            old_to_new[int(row["atom1_index"])], old_to_new[int(row["atom2_index"])]
        )
    output = builder.build()
    coordinates = msm.pyunitwizard.get_value(
        molsys.structures.coordinates, to_unit="nm"
    )[:, source_order, :]
    output.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(coordinates, "nm")
    )
    return output


def test_group_inventory_order_does_not_define_direction_or_cap_anchors():
    molsys = _reorder_groups(_peptide(), [2, 0, 1])
    report = msm.chemical_states.get_peptide_termini(molsys)
    np.testing.assert_array_equal(report["chains"][0]["group_indices"], [1, 2, 0])
    assert report["n_terminal_group_indices"].tolist() == [1]
    assert report["c_terminal_group_indices"].tolist() == [0]
    assert msm.build.get_missing_terminal_cappings(molsys) == {0: ["OXT"]}
    result = msm.build.add_missing_terminal_cappings(
        molsys, N_terminal="ACE", C_terminal="NME"
    )
    report = msm.chemical_states.get_peptide_termini(result)
    assert report["chains"][0]["n_capped"]
    assert report["chains"][0]["c_capped"]
    assert not len(report["n_terminal_group_indices"])
    assert not len(report["c_terminal_group_indices"])


def test_modular_file_recognition_does_not_load_coordinates_or_analyses(
    tmp_path, monkeypatch
):
    filename = tmp_path / "peptide.h5msm"
    molsys = _peptide()
    molsys.molecular_mechanics = None
    msm.convert(molsys, to_form="file:h5msm", output_filename=str(filename))
    import molsysmt.form._h5msm05_structures as structure_storage

    def forbidden(*args, **kwargs):
        pytest.fail("Static endpoint recognition must not load the structural series")

    monkeypatch.setattr(structure_storage, "read_independent_structures", forbidden)
    report = msm.chemical_states.get_peptide_termini(str(filename))
    assert report["c_terminal_group_indices"].tolist() == [2]


@pytest.mark.parametrize(
    "selection", [[0.1], [[0]], [True, 1], np.array([0], dtype=float)]
)
def test_invalid_selection_is_rejected_at_the_public_boundary(selection):
    with pytest.raises(msm.ArgumentError):
        msm.chemical_states.get_peptide_termini(_peptide(), selection=selection)


def test_explicit_partial_report_keeps_other_chains_and_never_invents_fragment_ends():
    from molsysmt._private.smonitor import UnassessedPeptideBackboneWarning

    molsys = msm.merge([_peptide(), _peptide()])
    pair = {_atom(molsys, 0, "C"), _atom(molsys, 1, "N")}
    bonds = molsys.chemical_states.get_bonds()
    index = next(
        i
        for i, row in bonds.iterrows()
        if {int(row["atom1_index"]), int(row["atom2_index"])} == pair
    )
    molsys.chemical_states.remove_bonds([int(index)])
    before = molsys.copy()
    with pytest.raises(msm.StructuralInconsistencyError, match="Disconnected"):
        msm.chemical_states.get_peptide_termini(molsys)
    report = msm.chemical_states.get_peptide_termini(molsys, on_ambiguous="report")
    assert report["unassessed_chain_indices"].tolist() == [0]
    assert report["n_terminal_group_indices"].tolist() == [3]
    assert report["c_terminal_group_indices"].tolist() == [5]
    row = report["chains"][0]
    assert row["status"] == "unassessed"
    assert row["n_terminal_group_index"] is row["c_terminal_group_index"] is None
    assert row["cyclic"] is None
    with pytest.warns(UnassessedPeptideBackboneWarning, match="Chain 0") as caught:
        assert msm.build.get_missing_terminal_cappings(molsys) == {5: ["OXT"]}
    assert "{chain_index}" not in str(caught[0].message)
    assert "{reason}" not in str(caught[0].message)
    assert molsys.chemical_states._inventory_equals(before.chemical_states)


@pytest.mark.parametrize("value", [None, True, 1, [], "ignore"])
def test_ambiguous_disposition_requires_an_explicit_supported_choice(value):
    with pytest.raises(msm.ArgumentError):
        msm.chemical_states.get_peptide_termini(_peptide(), on_ambiguous=value)


def test_an_explicit_dative_backbone_edge_is_not_a_peptide_bond():
    molsys = _peptide()
    pair = {_atom(molsys, 0, "C"), _atom(molsys, 1, "N")}
    bonds = molsys.chemical_states.get_bonds()
    index = next(
        i
        for i, row in bonds.iterrows()
        if {int(row["atom1_index"]), int(row["atom2_index"])} == pair
    )
    state = molsys.chemical_states._states[
        molsys.chemical_states.reference_chemical_state_index
    ]
    state.bonds["bond_type"] = "covalent"
    state.bonds.loc[index, ["bond_type", "joins_components"]] = ["dative", False]
    with pytest.raises(msm.StructuralInconsistencyError, match="Disconnected"):
        msm.chemical_states.get_peptide_termini(molsys)


def test_single_group_backbone_closure_is_not_a_free_amine_or_carboxyl():
    molsys = msm.build.build_peptide("Ala", engine="MolSysMT")
    molsys.chemical_states.add_bonds([[_atom(molsys, 0, "C"), _atom(molsys, 0, "N")]])
    report = msm.chemical_states.get_peptide_termini(molsys)
    assert report["chains"][0]["cyclic"]
    assert not len(report["n_terminal_group_indices"])
    assert not len(report["c_terminal_group_indices"])
