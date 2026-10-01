"""Prevent named observations from surviving public molecular geometry edits."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture
def observed_system():
    builder = msm.MolSysBuilder()
    for name, kind in [('N', 'N'), ('H', 'H'), ('O', 'O')]:
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2], group_name='ALA')
    builder.add_bond(0, 1)
    xyz = np.tile([[0, 0, 0], [.1, 0, 0], [.3, 0, 0]], (4, 1, 1))
    xyz[1, 2, 0] = .8
    builder.set_coordinates(msm.pyunitwizard.quantity(xyz, 'nm'))
    source = builder.build()
    msm.set(source, box=msm.pyunitwizard.quantity(np.tile(np.eye(3), (4, 1, 1)), 'nm'))
    msm.set(source, time=msm.pyunitwizard.quantity(np.arange(4), 'ps'))
    result = msm.interactions.hbonds.get_buch_hbonds(
        source, structure_indices=[2, 0, 1], pbc=False,
        output_type='molsysmt.Interactions',
    )
    source.interactions = {'buch': result, 'second': result.remap()}
    return source


def test_coordinate_edit_invalidates_real_observation_and_preserves_old_view(observed_system, tmp_path):
    source = observed_system
    originals = dict(source.interactions)
    previous_view = originals['buch'].query(structure_indices=[0])
    assert previous_view.n_interactions == 1

    msm.set(source, selection=[2], structure_indices=[0],
            coordinates=msm.pyunitwizard.quantity([[[10, 0, 0]]], 'angstrom'))

    for name, result in source.interactions.items():
        assert result.query(structure_indices=[0]).n_interactions == 0
        assert result.query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].size == 0
        assert result.query(structure_indices=[1]).n_interactions == 0
        np.testing.assert_array_equal(result.query(structure_indices=[1]).to_dict()['evaluated_structure_indices'], [1])
        assert result.query(structure_indices=[2]).n_interactions == 1
        assert result.query(structure_indices=[3]).to_dict()['evaluated_structure_indices'].size == 0
        assert result.parameters == originals[name].parameters
        assert result.software == originals[name].software
        assert result.measure_units == originals[name].measure_units
        np.testing.assert_array_equal(result.atom_source_indices, originals[name].atom_source_indices)
        np.testing.assert_array_equal(result.structure_source_indices, originals[name].structure_source_indices)
    assert previous_view.n_interactions == 1
    assert originals['buch'].query(structure_indices=[0]).n_interactions == 1
    fresh = msm.interactions.hbonds.get_buch_hbonds(
        source, pbc=False, output_type='molsysmt.Interactions')
    assert fresh.query(structure_indices=[0]).n_interactions == 0
    path = tmp_path / 'edited.h5msm'
    msm.convert(source, to_form='file:h5msm', output_filename=path)
    restored = msm.convert(path, to_form='molsysmt.MolSys')
    for result in restored.interactions.values():
        np.testing.assert_array_equal(result.query(structure_indices=[2, 0, 1]).to_dict()['evaluated_structure_indices'], [2, 1])
        assert result.query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].size == 0
        np.testing.assert_array_equal(result.query(structure_indices=[1]).to_dict()['evaluated_structure_indices'], [1])


@pytest.mark.parametrize('attribute', ['coordinates', 'box'])
@pytest.mark.parametrize('frames', [[2, 0, 2], [1], 'all'])
def test_geometry_edits_invalidate_exact_frame_coverage(observed_system, attribute, frames):
    source = observed_system
    coverage_before = {name: result.evaluated_structure_indices.tolist()
                       for name, result in source.interactions.items()}
    selected = list(range(4)) if frames == 'all' else frames
    shape = (len(selected), 3, 3)
    value = np.zeros(shape) if attribute == 'coordinates' else np.tile(2 * np.eye(3), (len(selected), 1, 1))
    msm.set(source, element='system', structure_indices=frames,
            **{attribute: msm.pyunitwizard.quantity(value, 'nm')})
    for name, result in source.interactions.items():
        expected = [frame for frame in coverage_before[name] if frame not in selected]
        np.testing.assert_array_equal(result.evaluated_structure_indices, expected)
        assert not np.isin(result.occurrence_structures, selected).any()


def test_noop_selections_and_non_geometry_edits_preserve_analyses(observed_system):
    source = observed_system
    original = source.interactions['buch']
    msm.set(source, structure_indices=[], coordinates=msm.pyunitwizard.quantity(np.empty((0, 3, 3)), 'nm'))
    msm.set(source, selection=[], structure_indices=[0], coordinates=msm.pyunitwizard.quantity(np.empty((1, 0, 3)), 'nm'))
    msm.set(source, structure_indices=[], box=msm.pyunitwizard.quantity(np.empty((0, 3, 3)), 'nm'))
    msm.set(source, structure_indices=[0], time=msm.pyunitwizard.quantity([5], 'ps'))
    assert source.interactions['buch'] is original


def test_invalid_structure_index_preserves_geometry_and_analyses(observed_system):
    source = observed_system
    original = source.interactions['buch']
    before = msm.pyunitwizard.get_value(msm.get(source, coordinates=True), to_unit='nm').copy()
    with pytest.raises(msm.ArgumentError):
        msm.set(source, structure_indices=[4], coordinates=msm.pyunitwizard.quantity(np.zeros((1, 3, 3)), 'nm'))
    assert source.interactions['buch'] is original
    np.testing.assert_array_equal(msm.pyunitwizard.get_value(msm.get(source, coordinates=True), to_unit='nm'), before)


def test_partial_delegate_failure_does_not_preserve_stale_coverage(observed_system, monkeypatch):
    from molsysmt.form.molsysmt_Structures import set as adapter

    original_setter = adapter.set_coordinates_to_atom

    def partially_failing_setter(*args, **kwargs):
        original_setter(*args, **kwargs)
        raise RuntimeError('Failure after geometry write')

    monkeypatch.setattr(adapter, 'set_coordinates_to_atom', partially_failing_setter)
    with pytest.raises(RuntimeError, match='after geometry write'):
        msm.set(observed_system, selection=[2], structure_indices=[0],
                coordinates=msm.pyunitwizard.quantity([[[1, 0, 0]]], 'nm'))
    assert observed_system.interactions['buch'].query(structure_indices=[0]).n_interactions == 0
    assert observed_system.interactions['buch'].query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].size == 0


def test_invalidation_allocation_failure_precedes_geometry_write(observed_system, monkeypatch):
    source = observed_system
    original = source.interactions['buch']
    before = msm.pyunitwizard.get_value(msm.get(source, coordinates=True), to_unit='nm').copy()

    def fail_allocation(*args, **kwargs):
        raise MemoryError('Staged invalidation failed')

    monkeypatch.setattr(source.interactions['second'], 'invalidate_structures', fail_allocation)
    with pytest.raises(MemoryError, match='Staged invalidation failed'):
        msm.set(source, selection=[2], structure_indices=[0],
                coordinates=msm.pyunitwizard.quantity([[[1, 0, 0]]], 'nm'))
    assert source.interactions['buch'] is original
    np.testing.assert_array_equal(msm.pyunitwizard.get_value(msm.get(source, coordinates=True), to_unit='nm'), before)


@pytest.mark.parametrize('attribute', ['coordinates', 'box'])
def test_geometry_axis_resize_is_rejected_before_changing_attached_system(observed_system, attribute):
    original = observed_system.interactions['buch']
    with pytest.raises(msm.StructuralInconsistencyError, match='cannot resize'):
        msm.set(observed_system, **{attribute: msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), 'nm')})
    assert observed_system.structures.n_structures == 4
    assert observed_system.interactions['buch'] is original


@pytest.mark.parametrize('in_place', [False, True])
def test_general_translation_uses_the_same_owner_invalidation(observed_system, in_place):
    source = observed_system
    transformed = msm.structure.translate(
        source, selection=[2], structure_indices=[0],
        translation=msm.pyunitwizard.quantity([[[.7, 0, 0]]], 'nm'),
        in_place=in_place,
    )
    target = source if in_place else transformed
    assert target.interactions['buch'].query(structure_indices=[0]).n_interactions == 0
    assert target.interactions['buch'].query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].size == 0
    assert target.interactions['buch'].query(structure_indices=[2]).n_interactions == 1
    if not in_place:
        assert source.interactions['buch'].query(structure_indices=[0]).n_interactions == 1


def test_clearing_box_invalidates_coverage_without_changing_axes(observed_system):
    msm.set(observed_system, box=None)
    assert msm.get(observed_system, box=True) is None
    assert observed_system.structures.n_structures == 4
    for result in observed_system.interactions.values():
        assert result.n_interactions == 0
        assert result.evaluated_structure_indices.size == 0
