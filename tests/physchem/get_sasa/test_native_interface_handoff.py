"""Receive fixed-geometry SASA contexts against independent sphere areas (#734)."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

TOLERANCE = json.loads(
    (
        Path(__file__).parents[2] / "scientific_truth/evidence/tolerances.json"
    ).read_text()
)["shrake_rupley_sampling_area_atol"]["atol"]


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
@pytest.mark.parametrize("cell_list", [False, True])
@pytest.mark.parametrize("far", [False, True])
def test_fixed_contexts_preserve_maps_chemistry_radii_and_spherical_cap_loss(
    native_interface_molsys, length, time, cell_list, far
):
    source = native_interface_molsys
    # Prepare the existing analytic 0.31-nm cap fixture before fixing the input.
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[2, 30, 0] = 3.31
    if far:
        xyz[2, [30, 10], 0] += 10
    msm.set(source, coordinates=puw.quantity(xyz, "nm"))
    before = source.copy()
    union = msm.extract(source, selection=[8, 2, 30, 10], structure_indices=[2])
    assert msm.get(union, element="atom", atom_id=True) == [
        "atom-2",
        "atom-8",
        "atom-10",
        "atom-30",
    ]
    first = msm.extract(union, selection=[0, 1])
    second = msm.extract(union, selection=[2, 3])
    options = dict(
        engine="MolSysMT",
        element="atom",
        structure_indices=[0],
        probe_radius="140 pm",
        n_sphere_points=960,
        pbc=False,
        use_gpu=False,
        use_cell_list=cell_list,
        parallel=False,
        num_threads=1,
    )
    with puw.context(standard_units=[length, time, "radians"]):
        policy = puw.configure.get_standard_units()
        united = msm.physchem.get_sasa(union, **options)
        a = msm.physchem.get_sasa(first, **options)
        b = msm.physchem.get_sasa(second, **options)
        output_a = msm.physchem.get_sasa(union, selection=[0, 1], **options)
        for area in [united, a, b, output_a]:
            assert puw.check(area, dimensionality={"[L]": 2})
        values = puw.get_value(united, to_unit="nm**2")
        np.testing.assert_array_equal(
            puw.get_value(output_a, to_unit="nm**2"), values[:, :2]
        )
        loss_a = puw.get_value(a - output_a, to_unit="nm**2")
        loss_b = puw.get_value(b, to_unit="nm**2") - values[:, 2:]
        radius = 0.31  # Independent carbon vdW (0.17 nm) plus probe (0.14 nm).
        sphere = 4 * np.pi * radius**2
        cap = 0 if far else 2 * np.pi * radius * (radius - 0.31 / 2)
        np.testing.assert_allclose(
            puw.get_value(a, to_unit="nm**2"), sphere, atol=1e-12
        )
        np.testing.assert_allclose(
            puw.get_value(b, to_unit="nm**2"), sphere, atol=1e-12
        )
        np.testing.assert_allclose(loss_a, [[cap, 0]], atol=TOLERANCE, rtol=0)
        np.testing.assert_allclose(loss_b, [[0, cap]], atol=TOLERANCE, rtol=0)
        total = loss_a.sum(axis=1) + loss_b.sum(axis=1)
        np.testing.assert_allclose(total, [2 * cap], atol=2 * TOLERANCE, rtol=0)
        np.testing.assert_allclose(total / 2, [cap], atol=TOLERANCE, rtol=0)
        assert np.all(loss_a >= 0) and np.all(loss_b >= 0)
        assert puw.configure.get_standard_units() == policy

    for context, indices in [
        (union, [2, 8, 10, 30]),
        (first, [2, 8]),
        (second, [10, 30]),
    ]:
        np.testing.assert_array_equal(
            puw.get_value(context.structures.coordinates, to_unit="nm"),
            xyz[[2]][:, indices],
        )
        assert msm.get(context, structure_chemical_state_index=True) == [1]
        np.testing.assert_array_equal(
            puw.get_value(msm.physchem.get_atomic_radius(context), to_unit="nm"),
            np.full(len(indices), 0.17),
        )
        assert msm.get(
            context,
            element="atom",
            chemical_state="structure",
            structure_indices=[0],
            formal_charge=True,
        ) == [1 if ii == 2 else -1 if ii == 30 else 0 for ii in indices]
    assert union.chemical_states.n_chemical_states == 2
    for state in [0, 1]:
        np.testing.assert_array_equal(
            msm.get(
                union, element="bond", bonded_atom_pairs=True, chemical_state=state
            ),
            [[0, 1], [2, 3]],
        )
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    assert (
        source.chemical_states.n_chemical_states
        == before.chemical_states.n_chemical_states
    )
    assert (
        source.chemical_states.reference_chemical_state_index
        == before.chemical_states.reference_chemical_state_index
    )
    for state in [0, 1]:
        pd.testing.assert_frame_equal(
            source.chemical_states.get_bonds(chemical_state=state),
            before.chemical_states.get_bonds(chemical_state=state),
        )
        np.testing.assert_array_equal(
            msm.get(source, element="atom", chemical_state=state, formal_charge=True),
            msm.get(before, element="atom", chemical_state=state, formal_charge=True),
        )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), xyz
    )


def test_third_body_is_not_removed_by_output_selection(native_interface_molsys):
    source = native_interface_molsys
    union = msm.extract(source, selection=[8, 2, 30, 10], structure_indices=[2])
    options = dict(
        engine="MolSysMT",
        n_sphere_points=960,
        probe_radius="0.14 nm",
        pbc=False,
        use_gpu=False,
        use_cell_list=False,
        parallel=False,
        num_threads=1,
    )
    in_source = msm.physchem.get_sasa(
        source, selection=[8], structure_indices=[2], **options
    )
    in_union = msm.physchem.get_sasa(
        union, selection=[1], structure_indices=[0], **options
    )
    assert (
        puw.get_value(in_source, to_unit="nm**2")[0, 0]
        < puw.get_value(in_union, to_unit="nm**2")[0, 0]
    )


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_unequal_spheres_keep_independent_side_losses(length, time):
    builder = msm.MolSysBuilder()
    for element in ["C", "H"]:
        atom = builder.add_atom(atom_name=element, atom_type=element)
        builder.add_group([atom], group_name="LIG")
    union = builder.build()
    distance = 0.31
    union.structures.coordinates = puw.quantity([[[0, 0, 0], [distance, 0, 0]]], "nm")
    radii = np.array([0.17, 0.11]) + 0.14
    plane = (distance**2 + radii[0] ** 2 - radii[1] ** 2) / (2 * distance)
    heights = radii - np.array([plane, distance - plane])
    expected = 2 * np.pi * radii * heights
    # Fixture-only budget: eight maximum-radius sphere patches at 960 points.
    # This is not a global accuracy/rotation bound for arbitrary atomic surfaces.
    budget = 8 * 4 * np.pi * radii.max() ** 2 / 960
    assert abs(expected[0] - expected[1]) > 2 * budget
    options = dict(
        engine="MolSysMT",
        structure_indices=[0],
        probe_radius="0.14 nm",
        n_sphere_points=960,
        pbc=False,
        use_gpu=False,
        use_cell_list=False,
        parallel=False,
        num_threads=1,
    )
    with puw.context(standard_units=[length, time, "radians"]):
        together = msm.physchem.get_sasa(union, **options)
        isolated = [
            msm.physchem.get_sasa(msm.extract(union, selection=[ii]), **options)
            for ii in [0, 1]
        ]
        separate = np.array(
            [puw.get_value(area, to_unit="nm**2")[0, 0] for area in isolated]
        )
        np.testing.assert_allclose(separate, 4 * np.pi * radii**2, rtol=0, atol=1e-12)
        observed = separate - puw.get_value(together, to_unit="nm**2")[0]
        np.testing.assert_allclose(observed, expected, rtol=0, atol=budget)
        assert observed[1] > observed[0]
        np.testing.assert_allclose(
            observed.sum(), expected.sum(), rtol=0, atol=2 * budget
        )
