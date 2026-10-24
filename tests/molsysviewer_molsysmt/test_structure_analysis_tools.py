"""Receive structural analyses through real views and independent result oracles."""

import inspect
import subprocess
import sys

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

puw = msm.pyunitwizard
NEW = (
    "get_symmetry_corrected_rmsd",
    "get_secondary_structure",
    "principal_component_analysis",
)
OLD = (
    "get_distances",
    "get_vectors",
    "get_center",
    "get_radius_of_gyration",
    "get_angles",
    "get_dihedral_angles",
    "get_rmsd",
    "get_least_rmsd",
    "get_principal_axes",
    "get_least_squares_plane",
    "get_maximum_distances",
    "get_contacts",
    "get_rmsf",
    "get_minimum_distances",
    "get_neighbors",
)
SCOPE = [2, 0, 2]
CHEM_SCOPE = [1, 2, 0, 1]


def xyz(view, selection="all", structures="all"):
    return puw.get_value(
        msm.get(
            view.molsys,
            element="atom",
            selection=selection,
            structure_indices=structures,
            coordinates=True,
        ),
        to_unit="nm",
    )


def preserve(view):
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=view.molsys.get_n_atoms(),
        n_structures=msm.get(view.molsys, n_structures=True),
        evaluated_structure_indices=[0, 1, 2],
        method="receiving.structure.analyses",
    )
    view.interactions.attach(analysis, name="preserve", assume_aligned=True)
    view.regions.add(selection=[0, 2], tag="source")


@pytest.fixture
def peptide():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
            preserve(view)
            yield view


@pytest.fixture
def chemistry():
    pytest.importorskip("rdkit")
    # The caller explicitly requests the chemistry-carrying conversion.
    molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"], to_form="rdkit.Mol")
    with msv.new_view(molsys, structure_indices=[0, 0, 0]) as view:
        coords = xyz(view).copy()
        types = np.asarray(msm.get(view.molsys, element="atom", atom_type=True))
        bonds = np.asarray(msm.get(view.molsys, element="atom", bonded_atom_pairs=True))
        pair = None
        for atom in range(view.molsys.get_n_atoms()):
            neighbors = [int(b if a == atom else a) for a, b in bonds if atom in (a, b)]
            hydrogens = [a for a in neighbors if types[a] == "H"]
            if len(hydrogens) > 1:
                pair = hydrogens[:2]
                break
        assert pair is not None
        coords[1, pair] = coords[0, pair[::-1]]
        coords[2] = coords[0] + [0.0, 0.0, 0.2]
        view.addons.molsysmt.basic.set(coordinates=puw.quantity(coords, "nm"))
        preserve(view)
        count = view.molsys.get_n_atoms()
        indices = np.arange(count)
        identity = np.column_stack((indices, indices))
        alternate = identity.copy()
        alternate[pair, 1] = alternate[pair[::-1], 1]
        yield view, np.stack((identity, alternate))


@pytest.mark.parametrize("name", NEW)
def test_signatures_namespace_digestion_and_native_help(peptide, name):
    native = inspect.signature(getattr(msm.structure, name))
    expected = list(native.parameters.values())[1:]
    if "skip_digestion" not in native.parameters:
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    bound = getattr(peptide.addons.molsysmt.structure, name)
    assert list(inspect.signature(bound).parameters.values()) == expected
    assert bound.digestion_plan is not None
    assert "current view.molsys" in inspect.getdoc(bound)
    assert "not a scene object" in inspect.getdoc(bound)
    # The transform receiving file guards the complete expanded namespace.
    assert set(NEW + OLD) <= set(dir(peptide.addons.molsysmt.structure))
    assert not hasattr(peptide.addons.molsysmt, name)
    if name == "get_secondary_structure":
        assert "native callable has no declared skip_digestion" in inspect.getdoc(bound)


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("weighted", [False, True])
@pytest.mark.parametrize("structures", [SCOPE, [0]])
def test_pca_reconstructs_independent_weighted_covariance(
    peptide, unit, weighted, structures
):
    atoms = [4, 0, 2]
    coords = xyz(peptide, atoms, structures)
    weights = np.array([1.0, 3.0, 2.0]) if weighted else None
    flat = coords.transpose(0, 2, 1).reshape(len(structures), 9)
    centered = flat - flat.mean(axis=0)
    if weighted:
        centered *= np.tile(np.sqrt(weights), 3)
    covariance = centered.T @ centered / len(structures)
    state, status, before = (
        peptide.export_state(),
        peptide.addons.molsysmt.get_sync_status(),
        xyz(peptide).copy(),
    )
    analysis = peptide.molsys.interactions["preserve"]
    with puw.context(standard_units=[unit, "ps", "radians"]):
        vectors, values = (
            peptide.addons.molsysmt.structure.principal_component_analysis(
                selection=atoms,
                structure_indices=structures,
                weights=weights,
                use_gpu=False,
            )
        )
        assert puw.get_unit(values) == puw.unit(unit) ** 2
    numeric = puw.get_value(values, to_unit="nm**2")
    np.testing.assert_allclose(
        numeric, np.linalg.eigvalsh(covariance)[::-1], atol=1e-12
    )
    np.testing.assert_allclose(vectors @ vectors.T, np.eye(9), atol=1e-12)
    np.testing.assert_allclose(
        vectors.T @ np.diag(numeric) @ vectors, covariance, atol=1e-12
    )
    assert vectors.shape == (9, 9) and values.shape == (9,)
    np.testing.assert_array_equal(xyz(peptide), before)
    if weighted:
        np.testing.assert_array_equal(weights, [1, 3, 2])
    assert (
        peptide.export_state() == state
        and peptide.addons.molsysmt.get_sync_status() == status
    )
    assert peptide.molsys.interactions["preserve"] is analysis


@pytest.mark.parametrize("simplified", [False, True])
@pytest.mark.parametrize("selection", ["all", [3, 1, 3], np.array([3, 1, 3])])
def test_secondary_structure_preserves_mdtraj_codes_group_scope_and_structures(
    peptide, simplified, selection
):
    md = pytest.importorskip("mdtraj")
    trajectory = msm.convert(
        peptide.molsys, to_form="mdtraj.Trajectory", structure_indices=SCOPE
    )
    expected = md.compute_dssp(trajectory, simplified=simplified).astype("U2")
    if not isinstance(selection, str):
        # This native observable interprets numeric selections at group level.
        groups = np.unique(selection)
        expected = expected[:, groups]
    state, before = peptide.export_state(), xyz(peptide).copy()
    # This integration-only flag must never bypass native scientific digestion.
    result = peptide.addons.molsysmt.structure.get_secondary_structure(
        selection=selection,
        structure_indices=SCOPE,
        simplified=simplified,
        engine="MDTraj",
        skip_digestion=True,
    )
    np.testing.assert_array_equal(result, expected)
    np.testing.assert_array_equal(
        result,
        msm.structure.get_secondary_structure(
            peptide.molsys,
            selection=selection,
            structure_indices=SCOPE,
            simplified=simplified,
        ),
    )
    assert result.dtype.kind == "U"
    np.testing.assert_array_equal(xyz(peptide), before)
    assert peptide.export_state() == state


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("mode", ["off", "force"])
@pytest.mark.parametrize("cached", [False, True])
def test_symmetry_pose_rmsd_matches_explicit_map_geometry_without_alignment(
    chemistry, unit, mode, cached
):
    view, candidates = chemistry
    before = xyz(view).copy()
    expected = np.array(
        [
            [
                np.sqrt(
                    np.mean(np.sum((before[s] - before[0, mapping[:, 1]]) ** 2, axis=1))
                )
                for mapping in candidates
            ]
            for s in CHEM_SCOPE
        ]
    )
    raw = np.sqrt(
        np.mean(np.sum((before[CHEM_SCOPE] - before[0]) ** 2, axis=2), axis=1)
    )
    kwargs = dict(
        selection="all",
        structure_indices=CHEM_SCOPE,
        baseline_atom_correspondence=candidates[0],
        heavy_mode=mode,
    )
    saved = None
    if cached:
        saved = view.addons.molsysmt.topology.get_atom_correspondences(
            selection="all",
            structure_indices=CHEM_SCOPE,
            candidate_atom_correspondences=candidates,
        )
        original_maps = saved["atom_correspondences"].copy()
        kwargs["correspondences"] = saved
    else:
        kwargs["candidate_atom_correspondences"] = candidates
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    analysis = view.molsys.interactions["preserve"]
    with puw.context(standard_units=[unit, "ps", "radians"]):
        with msm.configure.context(chunk_size=1, chunk_memory_fraction=None):
            result = view.addons.molsysmt.structure.get_symmetry_corrected_rmsd(
                **kwargs
            )
        assert puw.get_unit(result["rmsd"]) == puw.unit(unit)
        assert puw.get_unit(result["raw_rmsd"]) == puw.unit(unit)
    np.testing.assert_allclose(
        puw.get_value(result["rmsd"], to_unit="nm"), expected.min(axis=1), atol=1e-12
    )
    np.testing.assert_allclose(
        puw.get_value(result["raw_rmsd"], to_unit="nm"), raw, atol=1e-12
    )
    np.testing.assert_array_equal(result["structure_indices"], CHEM_SCOPE)
    assert result["alignment"] == "none" and result["periodic_imaging"] == "none"
    assert result["search_scope"] == "supplied_atom_correspondences"
    assert set(result["software"]) >= {"molsysmt", "rdkit"}
    assert result["attribution"]["schema"] == "molsysmt.scientific_attribution@1"
    assert (
        result["attribution"]["target"]
        == "molsysmt.structure.get_symmetry_corrected_rmsd"
    )
    assert result["attribution"]["items"]
    assert result["correspondences"] is not saved
    if saved is not None:
        result["correspondences"]["atom_correspondences"][:] = -1
        np.testing.assert_array_equal(saved["atom_correspondences"], original_maps)
    np.testing.assert_array_equal(xyz(view), before)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )
    assert view.molsys.interactions["preserve"] is analysis


def test_symmetry_external_reference_constraints_and_empty_scope_remain_native(
    chemistry,
):
    view, candidates = chemistry
    reference = msm.copy(view.molsys)
    ref = xyz(view).copy() + [0.1, 0.0, 0.0]
    msm.set(reference, coordinates=puw.quantity(ref, "nm"))
    args = dict(
        selection="all",
        structure_indices=[2, 0, 2],
        reference_molecular_system=reference,
        reference_structure_index=1,
        candidate_atom_correspondences=candidates[0],
        fixed_atom_correspondence=candidates[0, :1],
    )
    result = view.addons.molsysmt.structure.get_symmetry_corrected_rmsd(**args)
    expected = np.sqrt(
        np.mean(np.sum((xyz(view)[[2, 0, 2]] - ref[1]) ** 2, axis=2), axis=1)
    )
    np.testing.assert_allclose(puw.get_value(result["rmsd"], to_unit="nm"), expected)
    assert result["raw_rmsd"] is None and result["reference_structure_index"] == 1
    args["structure_indices"] = []
    empty = view.addons.molsysmt.structure.get_symmetry_corrected_rmsd(**args)
    assert empty["rmsd"].shape == (0,) and empty["structure_indices"].dtype == np.int64
    np.testing.assert_array_equal(
        puw.get_value(
            msm.get(reference, element="atom", coordinates=True), to_unit="nm"
        ),
        ref,
    )


@pytest.mark.parametrize(
    "name,args",
    [
        ("get_secondary_structure", {"engine": "unsupported-engine"}),
        (
            "principal_component_analysis",
            {"engine": "unsupported-engine", "use_gpu": False},
        ),
        ("get_symmetry_corrected_rmsd", {"method": "unsupported-method"}),
    ],
)
def test_native_errors_preserve_view_and_science(chemistry, name, args):
    view, _ = chemistry
    state, status, before = (
        view.export_state(),
        view.addons.molsysmt.get_sync_status(),
        xyz(view).copy(),
    )
    with pytest.raises(Exception) as error:
        getattr(msm.structure, name)(view.molsys, **args)
    with pytest.raises(type(error.value)):
        getattr(view.addons.molsysmt.structure, name)(**args)
    np.testing.assert_array_equal(xyz(view), before)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", NEW)
def test_controls_lifetime_and_primary_binding(peptide, name):
    method = getattr(peptide.addons.molsysmt.structure, name)
    with pytest.raises(TypeError):
        method(molecular_system=object(), skip_digestion=True)
    with pytest.raises(Exception):
        method(skip_digestion="yes")
    peptide.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(skip_digestion=True)
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.structure, name)()


@pytest.mark.parametrize(
    "name", ["get_secondary_structure", "principal_component_analysis"]
)
def test_cached_analysis_reader_uses_pending_data_and_replacement(peptide, name):
    method = getattr(peptide.addons.molsysmt.structure, name)
    args = (
        {}
        if name == "get_secondary_structure"
        else {"selection": [0, 2], "use_gpu": False}
    )
    coords = xyz(peptide).copy()
    coords[2, 0] += [0.1, 0.0, 0.0]
    peptide.addons.molsysmt.basic.set(
        coordinates=puw.quantity(coords, "nm"), update_view=False
    )
    status = peptide.addons.molsysmt.get_sync_status()
    assert status["state"] == "pending"
    actual, expected = (
        method(**args),
        getattr(msm.structure, name)(peptide.molsys, **args),
    )
    if name == "get_secondary_structure":
        np.testing.assert_array_equal(actual, expected)
    else:
        np.testing.assert_allclose(puw.get_value(actual[1]), puw.get_value(expected[1]))
    assert peptide.addons.molsysmt.get_sync_status() == status
    peptide.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as replacement:
        peptide.load(replacement.molsys, mode="replace")
    actual, expected = (
        method(**args),
        getattr(msm.structure, name)(peptide.molsys, **args),
    )
    if name == "get_secondary_structure":
        np.testing.assert_array_equal(actual, expected)
    else:
        np.testing.assert_allclose(puw.get_value(actual[1]), puw.get_value(expected[1]))


def test_discovery_keeps_optional_scientific_engines_lazy():
    code = "import sys; import molsysviewer_molsysmt.tools; assert 'rdkit' not in sys.modules; assert 'mdtraj' not in sys.modules"
    subprocess.run(
        [sys.executable, "-c", code], check=True, capture_output=True, text=True
    )


def test_cached_symmetry_reader_follows_pending_coordinates_and_replacement(chemistry):
    view, _ = chemistry
    reference = msm.copy(view.molsys)
    method = view.addons.molsysmt.structure.get_symmetry_corrected_rmsd
    kwargs = dict(
        selection="all", structure_indices=[0], reference_molecular_system=reference
    )
    view.addons.molsysmt.basic.set(
        coordinates=puw.quantity(xyz(view) + [0.1, 0.0, 0.0], "nm"), update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == "pending"
    result = method(**kwargs)
    np.testing.assert_allclose(puw.get_value(result["rmsd"], to_unit="nm"), [0.1])
    assert view.addons.molsysmt.get_sync_status() == status
    view.addons.molsysmt.sync_view()
    view.load(reference, mode="replace")
    np.testing.assert_allclose(
        puw.get_value(method(**kwargs)["rmsd"], to_unit="nm"), [0.0], atol=1e-12
    )


@pytest.mark.parametrize(
    "kind", ["list", "tuple", "int", "float32", "strided", "readonly", "percent"]
)
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_repaired_pca_weight_containers_preserve_covariance_and_inputs(
    peptide, kind, unit
):
    base = np.array([1.0, 4.0, 0.0])
    weights = {
        "list": lambda: base.tolist(),
        "tuple": lambda: tuple(base),
        "int": lambda: base.astype(np.int64),
        "float32": lambda: base.astype(np.float32),
        "strided": lambda: np.repeat(base, 2)[::2],
        "readonly": lambda: base.copy(),
        "percent": lambda: puw.quantity(base * 100, "percent"),
    }[kind]()
    if kind == "readonly":
        weights.flags.writeable = False
    before = np.asarray(
        puw.get_value(weights) if puw.is_quantity(weights) else weights
    ).copy()
    coords = xyz(peptide, [4, 0, 4], SCOPE)
    flat = np.concatenate([coords[:, :, axis] for axis in range(3)], axis=1)
    weighted = (flat - flat.mean(axis=0)) * np.sqrt(np.tile(base, 3))
    covariance = weighted.T @ weighted / len(SCOPE)
    state, status = peptide.export_state(), peptide.addons.molsysmt.get_sync_status()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        vectors, values = (
            peptide.addons.molsysmt.structure.principal_component_analysis(
                selection=[4, 0, 4],
                structure_indices=SCOPE,
                weights=weights,
                use_gpu=False,
            )
        )
        assert puw.get_unit(values) == puw.unit(unit) ** 2
    raw = puw.get_value(values, to_unit="nm**2")
    np.testing.assert_allclose(raw, np.linalg.eigvalsh(covariance)[::-1], atol=1e-12)
    np.testing.assert_allclose(
        vectors.T @ np.diag(raw) @ vectors, covariance, atol=1e-12
    )
    np.testing.assert_array_equal(
        puw.get_value(weights) if puw.is_quantity(weights) else weights, before
    )
    if kind == "readonly":
        assert weights.flags.writeable is False
    assert (
        peptide.export_state() == state
        and peptide.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize(
    "weights",
    [
        [1.0],
        [1.0, -1.0, 2.0],
        [0.0, 0.0, 0.0],
        [1.0, np.nan, 2.0],
        [1.0, np.inf, 2.0],
        puw.quantity([1.0, 2.0, 3.0], "nm"),
        "masses",
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_repaired_pca_invalid_weights_reject_without_scene_effects(
    peptide, weights, skip
):
    args = dict(
        selection=[4, 0, 4],
        structure_indices=SCOPE,
        weights=weights,
        use_gpu=False,
        skip_digestion=skip,
    )
    before, state = xyz(peptide).copy(), peptide.export_state()
    with pytest.raises(Exception) as native:
        msm.structure.principal_component_analysis(peptide.molsys, **args)
    with pytest.raises(type(native.value)):
        peptide.addons.molsysmt.structure.principal_component_analysis(**args)
    np.testing.assert_array_equal(xyz(peptide), before)
    assert peptide.export_state() == state
    assert peptide.addons.molsysmt.get_sync_status()["state"] == "synchronized"
