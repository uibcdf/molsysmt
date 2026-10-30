"""Receive native preparation audits without repairing or publishing a system."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError

import molsysmt as msm

puw = msm.pyunitwizard
GROUP_READERS = (
    "get_missing_heavy_atoms",
    "get_missing_terminal_cappings",
    "get_non_standard_residues",
)
NAMES = GROUP_READERS + (
    "get_missing_residues",
    "get_missing_bonds",
    "get_disulfide_bonds",
    "has_hydrogens",
    "is_solvated",
)
ORIGINAL = (
    "get_residue_chemical_coverage",
    "get_covalent_bond_candidates",
    "get_peptide_bond_candidates",
)


def _same(actual, expected):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            _same(actual[key], expected[key])
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for first, second in zip(actual, expected):
            _same(first, second)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.fixture(scope="module")
def source():
    with msv.demo["pentalanine"] as view:
        # The legacy demo stores unknown (-1) chain membership. This fixture
        # explicitly declares the chain required for terminal-capping audits.
        msm.set(
            view.molsys, element="atom", chain_index=[0] * view.molsys.get_n_atoms()
        )
        yield view.molsys


@pytest.fixture
def view(source):
    with msv.new_view(source, structure_indices=[0, 8, 3]) as view:
        view.regions.add(selection=[0, 2], tag="preserve")
        view.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=view.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.build.audit",
            ),
            name="preserve",
            assume_aligned=True,
        )
        yield view


def _kwargs(name):
    if name == "get_missing_residues":
        return {"sequence": {}}
    if name in {"get_missing_bonds", "get_disulfide_bonds"}:
        return {"structure_index": 2, "pbc": False}
    return {}


@pytest.mark.parametrize("name", NAMES)
def test_explicit_native_signature_and_local_only_skip_control(view, name):
    method = getattr(view.addons.molsysmt.build, name)
    signature = inspect.signature(getattr(msm.build, name))
    parameters = list(signature.parameters.values())[1:]
    if "skip_digestion" not in signature.parameters:
        parameters.append(
            inspect.Parameter(
                "skip_digestion",
                inspect.Parameter.KEYWORD_ONLY,
                default=False,
            )
        )
        assert "native callable receives no such parameter" in inspect.getdoc(method)
    assert inspect.signature(method) == signature.replace(parameters=parameters)
    assert method.digestion_plan is not None
    assert set(dir(view.addons.molsysmt.build)) == set(NAMES + ORIGINAL)
    assert not hasattr(view.addons.molsysmt, name)
    assert "not a scene object" in inspect.getdoc(method)
    for kwargs in [
        dict(update_view=False),
        dict(molecular_system=view.molsys),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**kwargs)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_native_values_and_source_scene_ownership_are_preserved(view, name, skip):
    primary = view.molsys
    atoms = primary.topology.copy().atoms
    bonds = primary.chemical_states._states[0].bonds.copy(deep=True)
    xyz = puw.get_value(primary.structures.coordinates).copy()
    analysis = deepcopy(primary.interactions["preserve"].to_dict())
    before = view.export_state()
    args = _kwargs(name)
    actual = getattr(view.addons.molsysmt.build, name)(**args, skip_digestion=skip)
    if "skip_digestion" in inspect.signature(getattr(msm.build, name)).parameters:
        args["skip_digestion"] = skip
    expected = getattr(msm.build, name)(primary, **args)
    assert actual == expected
    # Mutating a returned diagnostic must not alter a subsequent native result.
    if isinstance(actual, dict):
        actual.clear()
    elif isinstance(actual, list):
        actual.append([-1, -1])
    assert getattr(msm.build, name)(primary, **args) == expected
    assert primary is view.molsys and before == view.export_state()
    pd.testing.assert_frame_equal(atoms, primary.topology.atoms)
    pd.testing.assert_frame_equal(bonds, primary.chemical_states._states[0].bonds)
    np.testing.assert_array_equal(xyz, puw.get_value(primary.structures.coordinates))
    _same(primary.interactions["preserve"].to_dict(), analysis)


@pytest.mark.parametrize("name", GROUP_READERS)
@pytest.mark.parametrize("selection", [[1, 1], "group_index==1", []])
def test_native_group_selection_numeric_expression_and_empty(view, name, selection):
    assert getattr(view.addons.molsysmt.build, name)(selection=selection) == getattr(
        msm.build, name
    )(view.molsys, selection=selection)


def test_missing_heavy_atom_is_literal_and_not_repaired(source):
    molsys = msm.extract(
        source,
        selection="not (group_index==1 and atom_name=='CB')",
        structure_indices=[0],
    )
    with msv.new_view(molsys) as view:
        result = view.addons.molsysmt.build.get_missing_heavy_atoms(selection=[1])
        assert result == {1: ["CB"]}
        assert "CB" not in msm.get(
            view.molsys, selection="group_index==1", atom_name=True
        )
        assert view.addons.molsysmt.build.get_missing_heavy_atoms(selection=[]) == {}


def test_terminal_selected_scope_is_not_full_chain_proof():
    with msv.demo["181L"] as view:
        tools = view.addons.molsysmt.build
        assert tools.get_missing_terminal_cappings() == {161: ["OXT"]}
        # Native logic uses the selected groups, not an inferred whole-chain scope.
        assert tools.get_missing_terminal_cappings(selection=[0]) == {0: ["OXT"]}
        assert tools.get_missing_terminal_cappings(selection=[]) == {}


def test_nonstandard_suggestion_does_not_replace_or_certify_chemistry():
    builder = msm.MolSysBuilder()
    for name in ["MSE", "ALA", "UNK"]:
        atom = builder.add_atom(atom_name="CA", atom_type="C")
        builder.add_group([atom], group_name=name)
    builder.set_coordinates(puw.quantity(np.zeros((3, 3)), "nm"))
    with msv.new_view(builder.build()) as view:
        assert view.addons.molsysmt.build.get_non_standard_residues() == {0: "MET"}
        assert msm.get(view.molsys, element="group", group_name=True) == [
            "MSE",
            "ALA",
            "UNK",
        ]


def test_missing_sequence_reference_warning_and_explicit_chain_mapping():
    with msv.demo["181L"] as view:
        tools = view.addons.molsysmt.build
        with pytest.warns(UserWarning, match="no reference sequence"):
            assert tools.get_missing_residues() == {}
        chain_id = msm.get(view.molsys, element="chain", chain_id=True)[0]
        sequence = msm.get(
            view.molsys, element="group", selection="chain_index==0", group_name=True
        )
        reference = {chain_id: sequence + ["ASN", "LEU"]}
        before = deepcopy(reference)
        assert tools.get_missing_residues(sequence=reference) == {
            (0, len(sequence)): ["ASN", "LEU"]
        }
        assert reference == before
        assert tools.get_missing_residues(sequence={chain_id: sequence}) == {}


@pytest.mark.parametrize(
    "selection, expected",
    [("all", True), ("atom_type=='H'", True), ("atom_type!='H'", False), ([], False)],
)
def test_hydrogen_presence_does_not_claim_completeness(view, selection, expected):
    assert (
        bool(view.addons.molsysmt.build.has_hydrogens(selection=selection)) is expected
    )


def _sulfur_system(box=False):
    builder = msm.MolSysBuilder()
    for _ in range(2):
        atom = builder.add_atom(atom_name="SG", atom_type="S")
        builder.add_group([atom], group_name="CYS")
    coordinates = [[[0, 0, 0], [0.20, 0, 0]], [[0, 0, 0], [0.35, 0, 0]]]
    if box:
        coordinates = [[[0.95, 0, 0], [0.05, 0, 0]]]
    builder.set_coordinates(puw.quantity(coordinates, "nm"))
    if box:
        builder.set_box(puw.quantity(np.eye(3), "nm"))
    return builder.build()


def test_disulfide_singular_structure_selection_and_no_topology_insertion():
    with msv.new_view(_sulfur_system()) as view:
        tools = view.addons.molsysmt.build
        assert tools.get_disulfide_bonds(structure_index=0, pbc=False) == [[0, 1]]
        assert tools.get_disulfide_bonds(structure_index=1, pbc=False) == []
        assert (
            tools.get_disulfide_bonds(structure_index=0, selection=[0], pbc=False) == []
        )
        assert tools.get_disulfide_bonds(
            structure_index=1, max_bond_length="4 angstroms", pbc=False, sorted=False
        ) == [[0, 1]]
        assert msm.get(view.molsys, n_bonds=True) == 0
        with pytest.raises(Exception) as expected:
            msm.build.get_disulfide_bonds(view.molsys, structure_index=2)
        with pytest.raises(type(expected.value)):
            tools.get_disulfide_bonds(structure_index=2)
    with msv.new_view(_sulfur_system(box=True)) as view:
        tools = view.addons.molsysmt.build
        assert tools.get_disulfide_bonds(pbc=False) == []
        assert tools.get_disulfide_bonds(pbc=True) == [[0, 1]]


def test_missing_bonds_keep_source_atom_pairs_without_assignment(source):
    molsys = msm.copy(source)
    # Delete one declared bond on this independent source, without altering coordinates.
    pairs = msm.get(molsys, inner_bonded_atom_pairs=True)
    pair = list(pairs[0])
    molsys.chemical_states.remove_bonds([0])
    with msv.new_view(molsys, structure_indices=[0]) as view:
        tools = view.addons.molsysmt.build
        result = tools.get_missing_bonds(selection=pair, pbc=False)
        assert result == [list(pair)]
        assert tools.get_missing_bonds(selection=[pair[0]], pbc=False) == []
        assert tools.get_missing_bonds(selection=[], pbc=False) == []
        assert tuple(pair) not in {
            tuple(p) for p in msm.get(view.molsys, inner_bonded_atom_pairs=True)
        }


def _water_system(n_waters, length=None, structures=1):
    builder = msm.MolSysBuilder()
    for _ in range(n_waters):
        indices = [
            builder.add_atom(atom_name=name, atom_type=element)
            for name, element in [("O", "O"), ("H1", "H"), ("H2", "H")]
        ]
        builder.add_group(indices, group_name="HOH")
        builder.add_bond(indices[0], indices[1])
        builder.add_bond(indices[0], indices[2])
    builder.set_coordinates(puw.quantity(np.zeros((structures, n_waters * 3, 3)), "nm"))
    if length is not None:
        builder.set_box(
            puw.quantity(
                np.repeat((np.eye(3) * length)[None], structures, axis=0), "nm"
            )
        )
    return builder.build()


@pytest.mark.parametrize(
    "n_waters,length,expected",
    [(16, None, False), (15, 1, False), (16, 1, True), (16, 2, False)],
)
def test_solvation_native_density_threshold_is_not_solvent_preparation(
    n_waters, length, expected
):
    with msv.new_view(_water_system(n_waters, length)) as view:
        assert bool(view.addons.molsysmt.build.is_solvated()) is expected


@pytest.mark.parametrize("name", NAMES)
def test_pending_primary_replacement_and_closed_empty_lifetime(view, name):
    method = getattr(view.addons.molsysmt.build, name)
    view.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    method(**_kwargs(name))
    assert (
        view.addons.molsysmt.get_sync_status() == status
        and status["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    args = _kwargs(name)
    if "structure_index" in args:
        args["structure_index"] = 0
    assert method(**args) == getattr(msm.build, name)(view.molsys, **args)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**args)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, name)(**args)


@pytest.mark.parametrize(
    "name",
    GROUP_READERS
    + ("get_missing_residues", "get_missing_bonds", "get_disulfide_bonds"),
)
def test_unsupported_engine_keeps_native_rejection(view, name):
    kwargs = dict(_kwargs(name), engine="unsupported-receiving-engine")
    with pytest.raises(Exception) as expected:
        getattr(msm.build, name)(view.molsys, **kwargs)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.build, name)(**kwargs)


def test_external_hydrogen_selection_uses_native_syntax(view):
    pytest.importorskip("mdtraj")
    atom = msm.select(view.molsys, selection="atom_type=='H'")[0]
    assert view.addons.molsysmt.build.has_hydrogens(
        selection=f"index {atom}", syntax="MDTraj"
    )
    heavy_atom = msm.select(view.molsys, selection="atom_type!='H'")[0]
    assert not view.addons.molsysmt.build.has_hydrogens(
        selection=f"index {heavy_atom}", syntax="MDTraj"
    )
