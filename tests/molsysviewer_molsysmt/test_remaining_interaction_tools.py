"""Receive directed metals, compound aromatic participants and indexed-water paths."""

import inspect
from collections.abc import Mapping
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError
from rdkit import Chem

import molsysmt as msm

puw = msm.pyunitwizard
FAMILIES = ("metal_coordination", "pi_pi", "cation_pi", "water_bridges")
NAMES = {
    "metal_coordination": "get_metal_coordination",
    "pi_pi": "get_pi_pi_interactions",
    "cation_pi": "get_cation_pi_interactions",
    "water_bridges": "get_water_bridges",
}
ALL_FAMILIES = {
    "hbonds",
    "disulfides",
    "ionic",
    "hydrophobic",
    "halogen_bonds",
    *FAMILIES,
}


def ring():
    angles = np.arange(6) * np.pi / 3
    return np.column_stack((0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6)))


def water_system(order=1, directions=(True, True, True)):
    molecule = Chem.AddHs(Chem.MolFromSmiles("O.C=O.C=O" if order == 1 else "O.O.N.N"))
    source = msm.convert(molecule)
    xyz = np.zeros((molecule.GetNumAtoms(), 3))
    xyz[:, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
    hs = [
        sorted(
            a.GetIdx()
            for a in molecule.GetAtomWithIdx(i).GetNeighbors()
            if a.GetSymbol() == "H"
        )
        for i in range(molecule.GetNumAtoms())
    ]
    if order == 1:
        xyz[0] = [0, 0, 0]
        xyz[hs[0]] = [[0.1, 0, 0], [0, 0.1, 0]]
        xyz[2], xyz[4] = [0.3, 0, 0], [0, 0.3, 0]
        atoms = np.array([0, hs[0][0], 2, 0, hs[0][1], 4], dtype=np.int64)
        moving = list(Chem.GetMolFrags(molecule)[2])
    else:
        xyz[:4] = [[0, 0, 0], [0.3, 0, 0], [-0.3, 0, 0], [0.6, 0, 0]]
        xyz[hs[0]] = [[0, 0.1, 0], [0, -0.1, 0]]
        xyz[hs[1]] = [[0.3, 0.1, 0], [0.3, -0.1, 0]]
        left, right, forward = directions
        if left:
            xyz[hs[2][0]] = [-0.2, 0, 0]
            a = [2, hs[2][0], 0]
        else:
            xyz[hs[0][0]] = [-0.1, 0, 0]
            a = [0, hs[0][0], 2]
        if right:
            xyz[hs[3][0]] = [0.5, 0, 0]
            c = [3, hs[3][0], 1]
        else:
            xyz[hs[1][0]] = [0.4, 0, 0]
            c = [1, hs[1][0], 3]
        if forward:
            xyz[hs[0][1]] = [0.1, 0, 0]
            b = [0, hs[0][1], 1]
        else:
            xyz[hs[1][1]] = [0.2, 0, 0]
            b = [1, hs[1][1], 0]
        atoms = np.array([*a, *b, *c], dtype=np.int64)
        moving = [3, *hs[3]]
    frames = np.repeat(xyz[None], 3, axis=0)
    frames[1, moving] += [2, 2, 2]
    source.structures.append(
        coordinates=puw.quantity(frames, "nm"),
        structure_id=["external-90", "external-12", "external-500"],
    )
    return source, atoms


def system(family, *, edge=False, metal_smiles="[Zn+2].O"):
    if family == "water_bridges":
        return water_system()[0]
    if family == "metal_coordination":
        source = msm.convert(Chem.MolFromSmiles(metal_smiles))
        xyz = np.array(
            [
                [[0, 0, 0], [0.20, 0, 0]],
                [[0, 0, 0], [2, 0, 0]],
                [[0, 0, 0], [0.24, 0, 0]],
            ]
        )
    elif family == "pi_pi":
        source = msm.convert(Chem.MolFromSmiles("c1ccccc1.c1ccccc1"))
        xyz = np.array(
            [
                np.vstack((ring(), ring() + [0, 0, 0.35])),
                np.vstack((ring(), ring() + [0, 0, 2])),
                np.vstack(
                    (ring(), (ring()[:, [2, 1, 0]] if edge else ring()) + [0, 0, 0.4])
                ),
            ]
        )
    else:
        source = msm.convert(Chem.MolFromSmiles("c1ccccc1.[NH4+]"))
        xyz = np.array([np.vstack((ring(), [0, 0, z])) for z in [0.35, 2, 0.36]])
    source.structures.append(
        coordinates=puw.quantity(xyz, "nm"),
        structure_id=["external-90", "external-12", "external-500"],
    )
    return source


def options(family, normalized=False):
    if family != "pi_pi":
        return {}
    if normalized:
        return dict(
            distance_threshold=puw.quantity(0.6, "nm"),
            angle_threshold=puw.quantity(np.pi / 6, "radians"),
            offset_threshold=puw.quantity(0.2, "nm"),
            planarity_threshold=puw.quantity(0.02, "nm"),
        )
    return dict(
        distance_threshold=".6 nm",
        angle_threshold="30 degrees",
        offset_threshold=".2 nm",
        planarity_threshold=".02 nm",
    )


def scopes(family):
    if family == "metal_coordination":
        return [0], [1]
    if family == "pi_pi":
        return list(range(6)), list(range(6, 12))
    if family == "cation_pi":
        return [6], list(range(6))
    atoms = water_system()[1]
    return [0], np.setdiff1d(atoms, [0]).tolist()


def native(family):
    return getattr(getattr(msm.interactions, family), NAMES[family])


def bound(view, family):
    return getattr(getattr(view.addons.molsysmt.interactions, family), NAMES[family])


def same(actual, expected):
    if isinstance(expected, msm.Interactions):
        same(actual.to_dict(), expected.to_dict())
    elif isinstance(expected, Mapping):
        assert actual.keys() == expected.keys()
        for k in expected:
            same(actual[k], expected[k])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for a, b in zip(actual, expected):
            same(a, b)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.fixture(params=FAMILIES)
def view(request):
    with msv.new_view(system(request.param)) as result:
        result.regions.add(selection=[0], tag="preserve")
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.remaining",
            ),
            name="sentinel",
            assume_aligned=True,
        )
        yield request.param, result


def test_explicit_signatures_native_defaults_help_and_complete_family_navigation(view):
    family, value = view
    method = bound(value, family)
    signature = inspect.signature(native(family))
    assert inspect.signature(method) == signature.replace(
        parameters=list(signature.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert set(dir(value.addons.molsysmt.interactions)) == ALL_FAMILIES
    assert dir(getattr(value.addons.molsysmt.interactions, family)) == [NAMES[family]]
    assert not hasattr(value.addons.molsysmt, NAMES[family])
    doc = inspect.getdoc(method)
    assert "not a scene object" in doc and "experimental" in doc and "RSS" in doc
    for arguments in [
        dict(update_view=False),
        dict(molecular_system=value.molsys),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**options(family), **arguments)
    if family == "pi_pi":
        with pytest.raises(msm.ArgumentError, match="four explicit cutoffs"):
            method(pbc=False)
    else:
        assert isinstance(method(pbc=False), msm.Interactions)


@pytest.mark.parametrize("skip", [False, True])
def test_current_primary_native_parity_without_source_scene_or_named_mutation(
    view, skip
):
    family, value = view
    source = value.molsys
    before = value.export_state()
    atoms = source.topology.atoms.copy(deep=True)
    bonds = source.chemical_states._states[0].bonds.copy(deep=True)
    xyz = puw.get_value(source.structures.coordinates).copy()
    sentinel = source.interactions["sentinel"]
    saved = deepcopy(sentinel.to_dict())
    args = dict(
        options(family, normalized=skip),
        structure_indices=[2, 1, 0, 2],
        pbc=False,
        output_type="molsysmt.interactions",
        skip_digestion=skip,
    )
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = bound(value, family)(**args)
        expected = native(family)(source, **args)
    same(result, expected)
    assert result.n_interactions == 2 and result.occurrence_structures.tolist() == [
        0,
        2,
    ]
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    if family == "water_bridges":
        assert len(result.participant_roles) == 6
        for leg in [1, 2]:
            np.testing.assert_allclose(
                result.measurements[f"leg_{leg}_donor_acceptor_distance"], 0.3
            )
            np.testing.assert_allclose(
                result.measurements[f"leg_{leg}_hydrogen_acceptor_distance"], 0.2
            )
            np.testing.assert_allclose(
                result.measurements[f"leg_{leg}_dha_angle"], np.pi
            )
            assert result.measure_units[f"leg_{leg}_dha_angle"] == "radians"
    else:
        distances = {
            "metal_coordination": [0.2, 0.24],
            "pi_pi": [0.35, 0.4],
            "cation_pi": [0.35, 0.36],
        }[family]
        np.testing.assert_allclose(
            result.measurements["distance"], distances, atol=1e-12
        )
        assert result.measure_units["distance"] == "nm"
    if family == "metal_coordination":
        assert result.participant_roles == ("metal", "ligand")
    elif family == "pi_pi":
        assert result.participant_roles == ("ring_a", "ring_b")
        assert result.participant_atom_offsets.tolist() == [0, 6, 12]
        assert result.measure_units["plane_angle"] == "radians"
    elif family == "cation_pi":
        assert result.participant_roles == ("cation", "ring")
        assert result.participant_atoms.tolist() == [6, 0, 1, 2, 3, 4, 5]
        assert result.measure_units["cation_charge"] == "e"
    assert result.parameters["attribution"]["items"] and result.software["molsysmt"]
    assert value.molsys is source and value.export_state() == before
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    pd.testing.assert_frame_equal(source.chemical_states._states[0].bonds, bonds)
    np.testing.assert_array_equal(puw.get_value(source.structures.coordinates), xyz)
    assert (
        set(source.interactions) == {"sentinel"}
        and source.interactions["sentinel"] is sentinel
    )
    same(sentinel.to_dict(), saved)
    value.close()
    assert result.query().n_interactions == 2


@pytest.mark.parametrize(
    "mode,which,count",
    [
        ("internal", "both", 2),
        ("internal", "first", 0),
        ("incident", "first", 2),
        ("incident", "second", 2),
        ("between", "first", 2),
        ("between", "second", 2),
    ],
)
def test_compound_and_all_leg_membership_keep_native_scopes_and_reversed_selections(
    view, mode, which, count
):
    family, value = view
    first, second = scopes(family)
    if which == "second":
        first, second = second, first
    args = dict(
        options(family),
        structure_indices=[2, 0, 2],
        pbc=False,
        selection_mode=mode,
        selection=first + second if which == "both" else first,
    )
    if mode == "between":
        args["selection_2"] = second
    result = bound(value, family)(**args)
    same(result, native(family)(value.molsys, **args))
    assert (
        result.n_interactions == count
        and result.evaluated_structure_indices.tolist() == [0, 2]
    )
    if count:
        assert (
            result.query(atom_indices=first, mode="involving_selection").n_interactions
            == 2
        )
        assert (
            result.query(atom_indices=first, mode="within_selection").n_interactions
            == 0
        )
        assert (
            result.between_selections(first, second, exclusive=True).n_interactions == 2
        )


def test_empty_evaluated_unevaluated_and_filtered_occurrence_references(view):
    family, value = view
    method = bound(value, family)
    result = method(**options(family), structure_indices=[2, 0, 2], pbc=False)
    indices = result.query().to_dict()["occurrence_indices"]
    assert indices.dtype == np.int64 and len(np.unique(indices)) == 2
    for frame in [0, 2]:
        assert (
            result.query(structure_indices=[frame]).to_dict()["occurrence_indices"][0]
            in indices
        )
    empty = method(**options(family), structure_indices=[1], pbc=False)
    assert empty.n_interactions == 0 and empty.evaluated_structure_indices.tolist() == [
        1
    ]
    assert all(v.shape == (0,) for v in empty.measurements.values())
    unassessed = method(**options(family), structure_indices=[], pbc=False)
    assert unassessed.evaluated_structure_indices.tolist() == []


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_typed_result_and_explicit_independent_named_h5msm_storage(
    view, heavy_mode, tmp_path
):
    family, value = view
    args = dict(
        options(family), structure_indices=[2, 0, 2], pbc=False, heavy_mode=heavy_mode
    )
    typed = bound(value, family)(**args, output_type="molsysmt.InteractionsDict")
    assert msm.get_form(typed) == "molsysmt.InteractionsDict"
    result = msm.convert(typed, to_form="molsysmt.Interactions")
    same(result, native(family)(value.molsys, **args))
    assert result.execution_records
    copy = value.addons.molsysmt.basic.copy()
    copy.interactions = {**copy.interactions, "calculated": result}
    path = str(tmp_path / "observations.h5msm")
    msm.convert(copy, to_form=path)
    same(msm.convert(path).interactions["calculated"], result)
    assert set(value.molsys.interactions) == {"sentinel"}


def test_external_syntax_preserves_native_support_and_reference_state_limit(view):
    family, value = view
    args = dict(
        options(family),
        selection="index " + " ".join(map(str, range(value.molsys.get_n_atoms()))),
        syntax="MDTraj",
        structure_indices=[2, 0],
        pbc=False,
    )
    if family in {"pi_pi", "cation_pi"}:
        # Native code substitutes an integer state for the requested reference,
        # so basic.select rejects external syntax. No selector translation here.
        with pytest.raises(msm.ArgumentError, match="syntax"):
            native(family)(value.molsys, **args)
        with pytest.raises(msm.ArgumentError, match="syntax"):
            bound(value, family)(**args)
        assert bound(value, family)(**options(family), pbc=False).n_interactions == 2
        return
    result = bound(value, family)(**args)
    same(result, native(family)(value.molsys, **args))
    assert result.n_interactions == 2


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3) * 2,
        np.array([[0, 2, 0], [-2, 0, 0], [0, 0, 2]]),
        np.array([[2, 0.1, 0], [0, 2, 0.1], [0, 0, 2]]),
    ],
)
def test_periodic_compound_images_and_water_leg_geometries(view, box):
    family, value = view
    source = system(family)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    shifts = np.zeros((source.get_n_atoms(), 3), dtype=np.int64)
    if family == "pi_pi":
        shifts[6:] = [1, -1, 0]
    elif family == "cation_pi":
        shifts[6] = [1, -1, 0]
    elif family == "metal_coordination":
        shifts[1] = [1, -1, 0]
    else:
        actual = np.unique(water_system()[1])
        shifts[actual] = [[i % 3 - 1, i % 2, 0] for i in range(len(actual))]
    xyz += shifts @ box
    source.structures.coordinates = puw.quantity(xyz, "nm")
    source.structures.box = puw.quantity(np.repeat(box[None], 3, axis=0), "nm")
    value.load(source, mode="replace")
    result = bound(value, family)(**options(family), structure_indices=[0])
    same(result, native(family)(value.molsys, **options(family), structure_indices=[0]))
    assert result.n_interactions == 1
    offsets = result.participant_atom_offsets
    observed = [
        xyz[0, result.participant_atoms[offsets[i] : offsets[i + 1]]]
        + result.image_vectors[i] @ box
        for i in range(len(result.participant_roles))
    ]
    if family == "water_bridges":
        for branch in [0, 1]:
            d, h, a = [p[0] for p in observed[branch * 3 : branch * 3 + 3]]
            np.testing.assert_allclose(
                np.linalg.norm(d - a),
                result.measurements[f"leg_{branch + 1}_donor_acceptor_distance"][0],
            )
            np.testing.assert_allclose(np.linalg.norm(h - a), 0.2, atol=1e-12)
    else:
        a, b = observed
        distance = np.linalg.norm(a.mean(axis=0) - b.mean(axis=0))
        np.testing.assert_allclose(
            distance, result.measurements["distance"][0], atol=1e-12
        )


@pytest.mark.parametrize(
    "invalid",
    [
        dict(output_type="tuple"),
        dict(structure_indices=[3]),
        dict(selection_mode="between"),
        dict(selection_2=[1]),
        dict(method="energy"),
        dict(chemical_state=999),
    ],
)
def test_native_invalid_arguments_preserve_scene_and_error_type(view, invalid):
    family, value = view
    args = options(family)
    args.update(invalid)
    before = value.export_state()
    with pytest.raises(Exception) as error:
        native(family)(value.molsys, **args)
    with pytest.raises(type(error.value)):
        bound(value, family)(**args)
    assert value.export_state() == before and set(value.molsys.interactions) == {
        "sentinel"
    }


def test_pending_reads_cached_handles_primary_replacement_and_lifetime(view):
    family, value = view
    method = bound(value, family)
    value.addons.molsysmt.structure.translate(
        translation="[1,0,0] nm", in_place=True, update_view=False
    )
    status = value.addons.molsysmt.get_sync_status()
    same(
        method(**options(family), pbc=False),
        native(family)(value.molsys, **options(family), pbc=False),
    )
    assert (
        status["state"] == "pending"
        and value.addons.molsysmt.get_sync_status() == status
    )
    with pytest.raises(SystemEditPendingError):
        value.export_state()
    value.addons.molsysmt.sync_view()
    value.load(system(family), mode="replace")
    assert method(**options(family), pbc=False).n_interactions == 2
    value.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**options(family), pbc=False)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            bound(empty, family)(**options(family))


@pytest.mark.parametrize("family", ["pi_pi", "cation_pi"])
def test_partial_ring_selections_reject_without_implicit_completion(family):
    with msv.new_view(system(family)) as value:
        with pytest.raises(msm.ArgumentError, match="cuts"):
            bound(value, family)(
                **options(family),
                selection=[0, 6],
                selection_mode="incident",
                pbc=False,
            )
        assert not value.molsys.interactions


@pytest.mark.parametrize(
    "args",
    [
        dict(
            method="centroid_angle_offset", profile="least_squares", **options("pi_pi")
        ),
        dict(method="centroid_angle_offset", profile="three_atom_plane"),
        dict(method="plane_angle_intersection", profile="smarts_5_6"),
        dict(method="plane_angle_intersection", profile="aromatic_cycles"),
    ],
)
def test_pi_reference_profiles_and_custom_proposal_are_explicit_and_serializable(
    args, tmp_path
):
    with msv.new_view(system("pi_pi")) as value:
        result = bound(value, "pi_pi")(**args, pbc=False)
        same(result, native("pi_pi")(value.molsys, **args, pbc=False))
        assert result.n_interactions == 2
        clone = value.addons.molsysmt.basic.copy()
        clone.interactions = {"pi": result}
        path = str(tmp_path / "profile.h5msm")
        msm.convert(clone, to_form=path)
        same(msm.convert(path).interactions["pi"], result)


@pytest.mark.parametrize(
    "geometry,frames", [("parallel", [0]), ("edge_to_face", [2]), ("both", [0, 2])]
)
def test_pi_geometry_filter_keeps_parallel_and_edge_occurrences(geometry, frames):
    with msv.new_view(system("pi_pi", edge=True)) as value:
        result = bound(value, "pi_pi")(**options("pi_pi"), geometry=geometry, pbc=False)
        assert result.occurrence_structures.tolist() == frames
        same(
            result,
            native("pi_pi")(
                value.molsys, **options("pi_pi"), geometry=geometry, pbc=False
            ),
        )


@pytest.mark.parametrize(
    "args",
    [
        dict(method="centroid_distance_angle", profile="smarts_5_6"),
        dict(method="centroid_distance_offset", profile="three_atom_plane"),
        dict(
            method="centroid_angle_offset", profile="least_squares", **options("pi_pi")
        ),
    ],
)
def test_cation_reference_profiles_retain_distinct_plane_and_charge_rules(args):
    with msv.new_view(system("cation_pi")) as value:
        result = bound(value, "cation_pi")(**args, pbc=False)
        same(result, native("cation_pi")(value.molsys, **args, pbc=False))
        assert result.n_interactions == 2
        assert (
            result.measure_units["normal_angle"] == "radians"
            and result.measure_units["cation_charge"] == "e"
        )


@pytest.mark.parametrize(
    "directions",
    [(a, b, c) for a in [False, True] for b in [False, True] for c in [False, True]],
)
@pytest.mark.parametrize(
    "method,profile",
    [
        ("baker_hubbard", None),
        ("wernet_nilsson", None),
        ("donor_acceptor_distance_angle", "smarts_donor_acceptor"),
    ],
)
def test_two_water_exact_order_keeps_three_simultaneous_legs_and_directed_roles(
    directions, method, profile
):
    source, atoms = water_system(order=2, directions=directions)
    with msv.new_view(source) as value:
        args = dict(order=2, hbond_method=method, hbond_profile=profile, pbc=False)
        result = bound(value, "water_bridges")(**args)
        same(result, native("water_bridges")(value.molsys, **args))
        assert result.n_interactions == 2 and len(result.participant_roles) == 9
        np.testing.assert_array_equal(result.participant_atoms, atoms)
        for leg in [1, 2, 3]:
            np.testing.assert_allclose(
                result.measurements[f"leg_{leg}_donor_acceptor_distance"], 0.3
            )
            np.testing.assert_allclose(
                result.measurements[f"leg_{leg}_dha_angle"], np.pi
            )
        assert result.parameters["mediator_order"] == 2
        assert bound(value, "water_bridges")(order=1, pbc=False).n_interactions == 0
        assert not value.molsys.interactions


def test_metal_dative_assignment_is_not_created_removed_or_retyped():
    with msv.new_view(system("metal_coordination", metal_smiles="[Zn+2]<-O")) as value:
        before = value.molsys.chemical_states._states[0].bonds.copy(deep=True)
        assert before["bond_type"].tolist() == ["dative"]
        result = bound(value, "metal_coordination")(pbc=False)
        same(result, native("metal_coordination")(value.molsys, pbc=False))
        assert result.n_interactions == 2
        pd.testing.assert_frame_equal(
            value.molsys.chemical_states._states[0].bonds, before
        )


@pytest.mark.parametrize("family", FAMILIES)
def test_real_legacy_demo_preserves_missing_chemistry_rejection(family):
    with msv.demo["pentalanine"] as demo:
        with msv.new_view(demo.molsys, structure_indices=[0, 8, 3]) as value:
            args = dict(options(family), structure_indices=[2, 0], pbc=False)
            before = value.export_state()
            with pytest.raises(msm.StructuralInconsistencyError) as error:
                native(family)(value.molsys, **args)
            with pytest.raises(type(error.value)):
                bound(value, family)(**args)
            assert value.export_state() == before and not value.molsys.interactions
