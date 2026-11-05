"""Receive native nonbonded queries against independent pair energies."""

import inspect
from copy import deepcopy
from itertools import combinations

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_molecular_mechanics_tools import energy_units

NAME = "get_non_bonded_potential_energy"
puw = msm.pyunitwizard


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0]) as owner:
            yield owner


@pytest.fixture
def engine(monkeypatch):
    monkeypatch.setenv("OPENMM_CPU_THREADS", "1")
    return pytest.importorskip("openmm")


def pair_energies(molsys):
    """Evaluate the NoCutoff Coulomb/Lennard-Jones formula, including 1-4 terms.

    Parameters come from a separately constructed OpenMM force field, without
    calling MolSysMT mechanical calculations or their masking helpers. CODATA
    supplies the Coulomb factor in kJ nm/(mol e**2).
    """
    from openmm import app, unit
    from scipy.constants import Avogadro, elementary_charge, epsilon_0

    topology = msm.convert(molsys, to_form="openmm.Topology")
    model = app.ForceField("amber14-all.xml", "amber14/tip3p.xml").createSystem(
        topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds
    )
    force = next(f for f in model.getForces() if f.getName() == "NonbondedForce")
    xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm")[0]
    parameters = [
        (
            float(q.value_in_unit(unit.elementary_charge)),
            float(s.value_in_unit(unit.nanometer)),
            float(e.value_in_unit(unit.kilojoule_per_mole)),
        )
        for q, s, e in (
            force.getParticleParameters(i) for i in range(force.getNumParticles())
        )
    ]
    exceptions = {}
    for index in range(force.getNumExceptions()):
        a, b, q, s, e = force.getExceptionParameters(index)
        exceptions[tuple(sorted((a, b)))] = (
            float(q.value_in_unit(unit.elementary_charge**2)),
            float(s.value_in_unit(unit.nanometer)),
            float(e.value_in_unit(unit.kilojoule_per_mole)),
        )
    coulomb = Avogadro * elementary_charge**2 / (4 * np.pi * epsilon_0) * 1e6
    output = np.zeros((len(xyz), len(xyz)))
    for a, b in combinations(range(len(xyz)), 2):
        if (a, b) in exceptions:
            q, sigma, epsilon = exceptions[a, b]
        else:
            qa, sa, ea = parameters[a]
            qb, sb, eb = parameters[b]
            q, sigma, epsilon = qa * qb, (sa + sb) / 2, np.sqrt(ea * eb)
        distance = np.linalg.norm(xyz[a] - xyz[b])
        sr6 = (sigma / distance) ** 6
        output[a, b] = output[b, a] = coulomb * q / distance + 4 * epsilon * (
            sr6**2 - sr6
        )
    return output


def method(view):
    return getattr(view.addons.molsysmt.molecular_mechanics, NAME)


def test_native_signature_help_discovery_and_expert_controls():
    native = inspect.signature(getattr(msm.molecular_mechanics, NAME))
    with msv.new_view() as view:
        call = method(view)
        assert inspect.signature(call) == native.replace(
            parameters=list(native.parameters.values())[1:]
        )
        assert call.digestion_plan is not None
        assert NAME in dir(view.addons.molsysmt.molecular_mechanics)
        assert not hasattr(view.addons.molsysmt, NAME)
        assert "\nmolecular_system :" not in inspect.getdoc(call)
        assert "#561" in inspect.getdoc(call)
        for flag in ("molecular_system", "structure_indices", "update_view"):
            with pytest.raises(UnknownArgumentError):
                call(**{flag: None})


@pytest.mark.parametrize(
    "selection",
    [
        "all",
        [0, 2, 7, 15],
        "group_index in [0,1]",
        [],
        (15, 7, 2, 0),
        np.array([15, 7, 2, 0], dtype=np.int64),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("energy_unit", ["kJ/mol", "kcal/mol"])
def test_internal_energy_matches_independent_pair_sum(
    view, engine, selection, skip, energy_unit
):
    pairs = pair_energies(view.molsys)
    atoms = msm.select(view.molsys, selection=selection)
    expected = pairs[np.ix_(atoms, atoms)].sum() / 2
    with puw.context(standard_units=energy_units(energy_unit)):
        before = snapshot(view)
        policy = dict(puw.configure.get_standard_units())
        actual = method(view)(selection=selection, skip_digestion=skip)
        assert puw.is_quantity(actual) and np.shape(puw.get_value(actual)) == ()
        assert np.isfinite(puw.get_value(actual))
        assert puw.get_unit(actual) == puw.get_unit(
            puw.standardize(puw.quantity(1, energy_unit))
        )
        np.testing.assert_allclose(
            puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=2e-6, atol=2e-4
        )
        assert dict(puw.configure.get_standard_units()) == policy
        unchanged(view, before)


@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("skip", [False, True])
def test_disjoint_cross_energy_matches_pairs_and_partition_identity(
    view, engine, syntax, skip
):
    a, b = [0, 2, 7], [15, 19, 40]
    args = {"selection": a, "selection_2": b}
    if syntax == "MDTraj":
        args = {
            "selection": "index 0 or index 2 or index 7",
            "selection_2": "index 15 or index 19 or index 40",
        }
    before = snapshot(view)
    pairs = pair_energies(view.molsys)
    actual = method(view)(**args, syntax=syntax, skip_digestion=skip)
    expected = pairs[np.ix_(a, b)].sum()
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=2e-6, atol=2e-4
    )
    internal = method(view)

    def energy(atoms):
        return puw.get_value(internal(selection=atoms), to_unit="kJ/mol")

    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"),
        energy(a + b) - energy(a) - energy(b),
        rtol=2e-6,
        atol=2e-4,
    )
    unchanged(view, before)


def test_two_sided_group_matrix_matches_independent_pairs_and_keeps_inputs(
    view, engine
):
    args = dict(
        selection="all in groups of group_index in [0,1]",
        selection_2="all in groups of group_index in [4,5]",
    )
    before_args, before = deepcopy(args), snapshot(view)
    a = msm.select(view.molsys, selection=args["selection"])
    b = msm.select(view.molsys, selection=args["selection_2"])
    pairs = pair_energies(view.molsys)
    expected = np.array([[pairs[np.ix_(x, y)].sum() for y in b] for x in a])
    actual = method(view)(**args)
    assert np.shape(puw.get_value(actual)) == (2, 2)
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"), expected, rtol=2e-6, atol=2e-4
    )
    assert args == before_args
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_native_mixed_partition_failure_is_retained_without_compensation(
    view, engine, skip
):
    args = dict(
        selection="all in groups of group_index in [0,1]",
        selection_2=[40, 41],
        skip_digestion=skip,
    )
    before = snapshot(view)
    with pytest.raises(TypeError) as native:
        getattr(msm.molecular_mechanics, NAME)(view.molsys, **args)
    with pytest.raises(type(native.value)) as actual:
        method(view)(**args)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"engine": "invalid"},
        {"platform": "Reference"},
        {"selection": [100000]},
        {"selection": "invalid_selection"},
    ],
)
def test_native_rejection_preserves_source_scene_and_diagnostic(
    view, engine, parameters
):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        getattr(msm.molecular_mechanics, NAME)(view.molsys, **parameters)
    with pytest.raises(type(native.value)) as actual:
        method(view)(**parameters)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


def test_pending_geometry_is_read_without_projection_or_history_changes(view, engine):
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy()
    xyz[0, 0, 0] += 0.001
    view.addons.molsysmt.basic.set(
        coordinates=puw.quantity(xyz, "nm"), update_view=False
    )
    before = snapshot(view)
    actual = method(view)()
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit="kJ/mol"),
        pair_energies(view.molsys).sum() / 2,
        rtol=2e-6,
        atol=2e-4,
    )
    unchanged(view, before)


def test_cached_reader_rebinds_and_rejects_empty_closed_owners(view, engine):
    call = method(view)
    first = puw.get_value(call(), to_unit="kJ/mol")
    replacement = view.molsys.copy()
    xyz = puw.get_value(replacement.structures.coordinates, to_unit="nm").copy()
    xyz[0, 0, 0] += 0.001
    msm.set(replacement, coordinates=puw.quantity(xyz, "nm"))
    view.load(replacement, mode="replace")
    before = snapshot(view)
    actual = puw.get_value(call(), to_unit="kJ/mol")
    assert not np.isclose(first, actual)
    np.testing.assert_allclose(
        actual, pair_energies(view.molsys).sum() / 2, rtol=2e-6, atol=2e-4
    )
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        call()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            method(empty)()
