"""Replacing frames must preserve sparse queries, provenance and bounded edits."""

import gc
import pickle
import tracemalloc
import weakref

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


def record(frame, value, atoms=(0, 1), kind='ionic', images=None, evidence='synthetic'):
    return dict(structure_index=frame, interaction_type=kind,
                participants=[dict(role='positive', atom_indices=list(atoms[:-1])),
                              dict(role='negative', atom_indices=[atoms[-1]])],
                evidence=evidence, measurements={'distance': value},
                **({} if images is None else {'images': images}))


def result(records, coverage, **changes):
    options = dict(n_atoms=6, n_structures=5, evaluated_structure_indices=coverage,
                   method='synthetic', parameters={'cutoff': {'value': .5, 'unit': 'nm'}},
                   software={'producer': '1.2'}, source_id='fixture',
                   measure_units={'distance': 'nm'})
    options.update(changes)
    return msm.Interactions.from_records(records, **options)


@pytest.mark.parametrize('periodic', [False, True])
def test_replacement_handles_new_relations_empty_frames_and_parallel_images(periodic, tmp_path):
    images = [[0, 0, 0], [1, 0, 0]] if periodic else None
    old = result([record(0, .1, images=images), record(2, .2, images=images),
                  record(4, .4, images=images)], [4, 0, 1, 2])
    previous = old.query(structure_indices=[2])
    fresh = result([record(2, .3, (2, 3, 4), kind='ring', images=images, evidence='new'),
                    record(2, .35, (2, 3, 4), kind='ring', images=images, evidence='new'),
                    record(3, .45, images=images)], [2, 0, 3])
    edited = old.replace_structures(fresh)
    data = edited.query(structure_indices=[4, 2, 0, 3, 2]).to_dict()
    np.testing.assert_array_equal(data['evaluated_structure_indices'], [4, 2, 0, 3])
    np.testing.assert_array_equal(data['occurrence_indices'], [3, 0, 1, 2])
    np.testing.assert_allclose(data['measurements']['distance'], [.4, .3, .35, .45])
    assert data['evidence'].tolist() == ['synthetic', 'new', 'new', 'synthetic']
    assert edited.query(structure_indices=[0]).n_interactions == 0
    assert edited.query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].tolist() == [0]
    assert previous.to_dict()['measurements']['distance'].tolist() == [.2]
    assert edited._packed_result is None
    assert edited.relation(1)['participants'][0]['atom_indices'].tolist() == [2, 3]
    for mode, atoms, values in [('incident', [2], [.3, .35]),
                                ('internal', [2, 3, 4], [.3, .35]),
                                ('cross', [2, 3], [.3, .35])]:
        selected = edited.query(atom_indices=atoms, mode=mode).to_dict()
        np.testing.assert_allclose(selected['measurements']['distance'], values)
        np.testing.assert_array_equal(selected['occurrence_indices'], [0, 1])
    assert edited.between([2], [4], exclusive=True).n_interactions == 0
    assert edited.between([2, 3], [4], exclusive=True).n_interactions == 2
    assert edited.query(atom_indices=[0], structure_indices=[4, 3]).to_dict()['occurrence_indices'].tolist() == [3, 2]
    assert edited._packed_result is None

    path = tmp_path / 'replaced.h5i'
    edited.save(path)
    payload = msm.convert(edited, to_form='molsysmt.InteractionsDict')
    file = tmp_path / 'replaced.h5msm'
    msm.h5msm.write_layers(file, interactions={'analysis': edited})
    restored = [msm.Interactions.load(path), pickle.loads(pickle.dumps(edited)),
                msm.convert(payload, to_form='molsysmt.Interactions'),
                msm.convert(file, to_form='molsysmt.MolSys').interactions['analysis']]
    for candidate in restored:
        actual = candidate.query(structure_indices=[4, 2, 0, 3, 2]).to_dict()
        for key in ('occurrence_indices', 'structure_indices', 'relation_indices', 'evidence'):
            np.testing.assert_array_equal(actual[key], data[key])
        np.testing.assert_allclose(actual['measurements']['distance'], data['measurements']['distance'])
        if periodic:
            np.testing.assert_array_equal(actual['image_offsets'], data['image_offsets'])
            np.testing.assert_array_equal(actual['image_vectors'], data['image_vectors'])
        assert candidate.parameters == old.parameters
        assert candidate.software == old.software
    assert edited._packed_result is None
    view = pickle.loads(pickle.dumps(edited.query(structure_indices=[4, 2])))
    assert view.to_dict()['occurrence_indices'].tolist() == [3, 0, 1]
    assert view.query(structure_indices=[3]).n_interactions == 0


@pytest.mark.parametrize('changes, field', [
    ({'method': 'other'}, 'method'), ({'parameters': {'cutoff': .3}}, 'parameters'),
    ({'software': {'producer': '2'}}, 'software'),
    ({'measure_units': {'distance': 'angstrom'}}, 'measure_units'),
    ({'source_id': 'other'}, 'source_id'), ({'n_atoms': 7}, 'n_atoms'),
    ({'n_structures': 6}, 'n_structures'),
    ({'atom_source_indices': [1, 0, 2, 3, 4, 5]}, 'atom_source_indices'),
    ({'structure_source_indices': [1, 0, 2, 3, 4]}, 'structure_source_indices'),
    ({'evaluation_mode': 'incident', 'evaluation_atom_indices': [0]}, 'evaluation_scope'),
])
def test_incompatible_replacement_is_rejected(changes, field):
    old = result([], [0])
    fresh = result([], [0], **changes)
    with pytest.raises(ValueError, match=field):
        old.replace_structures(fresh)
    assert old.evaluated_structure_indices.tolist() == [0]


def test_queries_cannot_be_replacement_operands_and_digestion_checks_type():
    old = result([], [0])
    with pytest.raises(ValueError, match='full'):
        old.replace_structures(old.query())
    with pytest.raises(ValueError, match='full'):
        old.query().replace_structures(old)
    with pytest.raises(ArgumentError, match='replacement'):
        old.replace_structures({})
    with pytest.raises(TypeError, match='Interactions'):
        old.replace_structures({}, skip_digestion=True)


def test_periodic_image_presence_is_checked_only_for_retained_populated_frames():
    old = result([record(0, .1, images=[[0, 0, 0], [1, 0, 0]])], [0])
    fresh = result([record(1, .2)], [1])
    with pytest.raises(ValueError, match='periodic images'):
        old.replace_structures(fresh)
    replaced = old.replace_structures(result([record(0, .3)], [0]))
    assert replaced.image_vectors is None
    empty = old.replace_structures(result([], [0]))
    assert empty.n_interactions == 0
    assert empty.query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].tolist() == [0]


def test_zero_observations_release_source_blocks_including_evaluated_empty_frames():
    old = result([record(0, .1)], [0, 1])
    reference = weakref.ref(old)
    edited = old.replace_structures(result([], [0]))
    del old
    gc.collect()
    assert reference() is None
    assert edited.evaluated_structure_indices.tolist() == [0, 1]
    assert edited.n_interactions == 0


def test_repeated_edits_and_invalidation_release_overridden_blocks_and_keep_old_views():
    old = result([record(0, .1), record(4, .4)], [0, 4])
    fresh = result([record(0, .2, (2, 3))], [0])
    reference = weakref.ref(fresh)
    first = old.replace_structures(fresh)
    view = first.query(structure_indices=[0])
    second = first.replace_structures(result([record(0, .3, (3, 4))], [0]))
    del first, fresh
    gc.collect()
    assert reference() is None  # A selected view owns only its selected rows.
    assert view.to_dict()['measurements']['distance'].tolist() == [.2]
    assert len(second._segments) == 2
    invalid = second.invalidate_structures([0])
    assert invalid.query(atom_indices=[3]).n_interactions == 0
    assert invalid.to_dict()['occurrence_indices'].tolist() == [0]
    assert invalid.query(structure_indices=[4]).n_interactions == 1
    filled = invalid.replace_structures(result([], [0]))
    assert filled.query(structure_indices=[0]).to_dict()['evaluated_structure_indices'].tolist() == [0]
    remapped = second.remap(atom_indices=[4, 3, 0, 1], structure_indices=[4, 0])
    assert remapped.to_dict()['measurements']['distance'].tolist() == [.4, .3]
    assert remapped.relation(1)['participants'][0]['atom_indices'].tolist() == [1]
    assert second._packed_result is None


def test_replacement_after_invalidation_shares_base_and_metadata_is_independent():
    old = result([record(0, .1), record(4, .4)], [0, 4])
    invalid = old.invalidate_structures([0])
    fresh = result([record(0, .2)], [0])
    edited = invalid.replace_structures(fresh)
    assert edited._segments[0][0] is old
    assert edited._segments[1][0] is fresh
    edited.parameters['cutoff']['value'] = .7
    assert old.parameters['cutoff']['value'] == .5
    assert fresh.parameters['cutoff']['value'] == .5
    assert edited.query().parameters['cutoff']['value'] == .7
    with pytest.raises(ValueError):
        edited.query().measurements['distance'][0] = 9


def test_selected_frame_routes_only_to_its_owner_and_shares_relation_registry(monkeypatch):
    old = result([record(0, .1), record(4, .4)], [0, 4])
    fresh = result([record(0, .2, (2, 3))], [0])
    edited = old.replace_structures(fresh)

    def unrelated_query(*args, **kwargs):
        raise AssertionError('A frame query visited an unrelated source block')

    with monkeypatch.context() as patch:
        patch.setattr(old, 'query', unrelated_query)
        view = edited.query(structure_indices=[0])
        assert view.to_dict()['measurements']['distance'].tolist() == [.2]
        assert view.participant_atoms is edited.participant_atoms
    query = old.query

    def active_only_query(*args, **kwargs):
        assert np.asarray(kwargs['structure_indices']).tolist() == [4]
        return query(*args, **kwargs)

    monkeypatch.setattr(old, 'query', active_only_query)
    assert edited.query().n_interactions == 2


def test_replacing_one_frame_does_not_copy_large_occurrence_tables():
    def large(count):
        return msm.Interactions(n_atoms=2, n_structures=10,
            evaluated_structure_indices=list(range(10)), method='synthetic',
            relation_types=['ionic'], relation_participant_offsets=[0, 2],
            participant_roles=['positive', 'negative'], participant_atom_offsets=[0, 1, 2],
            participant_atoms=[0, 1], occurrence_structures=np.arange(count) * 10 // count,
            occurrence_relations=np.zeros(count, dtype=np.int64),
            occurrence_evidence=np.zeros(count, dtype=np.int32), evidence_labels=['synthetic'],
            measurements={'distance': np.full(count, .2)}, measure_units={'distance': 'nm'})
    fresh = msm.Interactions.from_records([record(0, .3)], n_atoms=2, n_structures=10,
        evaluated_structure_indices=[0], method='synthetic', measure_units={'distance': 'nm'})
    peaks = []
    for count in (100, 200_000):
        old = large(count)
        tracemalloc.start()
        edited = old.replace_structures(fresh)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peaks.append(peak)
        assert edited._segments[0][0] is old
        assert edited._packed_result is None
        assert edited.query(structure_indices=[0]).n_interactions == 1
    assert max(peaks) < 100_000
    assert abs(peaks[1] - peaks[0]) < 30_000


def test_unchanged_registry_and_block_maps_are_shared_across_edits_and_invalidation():
    old = result([record(0, .1), record(4, .4)], [0, 1, 4])
    first = old.replace_structures(result([record(0, .2, (2, 3))], [0]))
    second = first.replace_structures(result([record(1, .3, (2, 3))], [1]))
    for name in ('relation_types', 'participant_roles', 'relation_participant_offsets',
                 'participant_atom_offsets', 'participant_atoms', 'evidence_labels'):
        assert getattr(second, name) is getattr(first, name)
    assert second.evaluated_structure_indices is first.evaluated_structure_indices
    assert second._relation_key_index is first._relation_key_index
    for first_segment, second_segment in zip(first._segments, second._segments):
        assert first_segment[2] is second_segment[2]
        assert first_segment[3] is second_segment[3]
    # First patch owns only frame 0, so its frame vector is unchanged too.
    assert first._segments[1][1] is second._segments[1][1]
    invalid = second.invalidate_structures([0])
    assert invalid.participant_atoms is second.participant_atoms
    assert invalid._relation_key_index is second._relation_key_index
    assert invalid.query().to_dict()['measurements']['distance'].tolist() == [.3, .4]
    for array in second._relation_key_index:
        with pytest.raises(ValueError):
            array.flags.writeable = True


def test_fingerprint_collisions_never_merge_distinct_typed_relations(monkeypatch, tmp_path):
    from molsysmt.interactions import _frame_replacement

    monkeypatch.setattr(_frame_replacement, '_fingerprint', lambda key: 0)
    old = result([record(0, .1), record(4, .4, (2, 3))], [0, 4])
    changed_role = record(0, .35, (2, 3))
    changed_role['participants'][0]['role'] = 'ring'
    first = old.replace_structures(result([
        record(0, .2, (2, 3)), record(0, .3, (1, 2, 3)), changed_role,
    ], [0]))
    second = first.replace_structures(result([
        record(1, .5, (1, 2, 3)), record(1, .6, (2, 3), kind='ring'),
    ], [1]))
    assert len(first.relation_types) == 4
    assert len(second.relation_types) == 5
    assert second.query(atom_indices=[1, 2, 3], mode='internal').n_interactions == 6
    observed = second.query(structure_indices=[1, 0, 4]).to_dict()
    path = tmp_path / 'collision.h5i'
    second.save(path)
    restored = msm.Interactions.load(path)
    np.testing.assert_array_equal(restored.query(structure_indices=[1, 0, 4]).to_dict()['relation_indices'],
                                  observed['relation_indices'])
    for index in range(5):
        a, b = second.relation(index), restored.relation(index)
        assert a['interaction_type'] == b['interaction_type']
        for ap, bp in zip(a['participants'], b['participants']):
            assert ap['role'] == bp['role']
            np.testing.assert_array_equal(ap['atom_indices'], bp['atom_indices'])
    assert first.query(structure_indices=[1]).n_interactions == 0


def test_equivalent_complete_catalog_uses_implicit_identity_without_key_index():
    old = result([record(0, .1)], [0])
    edited = old.replace_structures(result([record(1, .2)], [1]))
    assert edited._segments[0][2] is None
    assert edited._segments[1][2] is None
    assert not hasattr(edited, '_relation_key_index')
    assert edited.participant_atoms is old.participant_atoms
    assert edited.query().to_dict()['relation_indices'].tolist() == [0, 0]


def test_new_evidence_keeps_relation_buffers_and_translates_parallel_observations():
    old = result([record(0, .1), record(4, .4)], [0, 4])
    fresh = result([record(0, .2, evidence='external'), record(0, .3)], [0])
    edited = old.replace_structures(fresh)
    assert edited.participant_atoms is old.participant_atoms
    assert not hasattr(edited, '_relation_key_index')
    assert edited.evidence_labels == ('synthetic', 'external')
    data = edited.query().to_dict()
    assert data['evidence'].tolist() == ['external', 'synthetic', 'synthetic']
    np.testing.assert_allclose(data['measurements']['distance'], [.2, .3, .4])
    assert old.evidence_labels == ('synthetic',)
