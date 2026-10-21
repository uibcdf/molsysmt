"""Native copying must preserve sparse identity, ownership and lazy results."""

import copy
from types import MappingProxyType

import numpy as np
import pytest

import molsysmt as msm


def _native_copy(result):
    return result.copy()


def _analysis(records=None, coverage=(0, 1, 3)):
    if records is None:
        records = [
            _record(0, 0.2),
            _record(0, 0.21, shift=-1),
            _record(3, 0.4, atoms=((2, 3), (4, 5))),
        ]
    return msm.Interactions.from_records(
        records,
        n_atoms=6,
        n_structures=5,
        evaluated_structure_indices=coverage,
        atom_source_indices=[5, 4, 3, 2, 1, 0],
        structure_source_indices=[4, 3, 2, 1, 0],
        method="synthetic",
        parameters={"cutoff": {"value": 0.5, "unit": "nm"}},
        measure_units={"distance": "nm"},
        software={"producer": "0.1"},
        execution={"chunk_size": 2},
    )


def _record(structure, distance, atoms=((0,), (1,)), shift=1):
    return {
        "structure_index": structure,
        "interaction_type": "synthetic",
        "participants": [
            {"role": "a", "atom_indices": atoms[0]},
            {"role": "b", "atom_indices": atoms[1]},
        ],
        "measurements": {"distance": distance},
        "evidence": "synthetic geometry",
        "images": [[0, 0, 0], [shift, 0, 0]],
    }


@pytest.fixture(params=["full", "view", "filtered", "filtered_view", "patched"])
def analysis(request):
    source = _analysis()
    if request.param == "filtered":
        return source.invalidate_structures([0])
    if request.param == "filtered_view":
        return source.invalidate_structures([1]).query(structure_indices=[3, 0])
    if request.param == "patched":
        return source.replace_structures(
            _analysis([_record(0, 0.3, atoms=((2, 3), (4, 5)))], coverage=[0, 1])
        )
    if request.param == "view":
        return source.query(structure_indices=[3, 1, 0, 3])
    return source


def _equal(actual, expected):
    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected)
        assert actual.dtype == expected.dtype
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            _equal(actual[key], expected[key])
    elif isinstance(expected, (tuple, list)):
        assert type(actual) is type(expected)
        assert len(actual) == len(expected)
        for first, second in zip(actual, expected):
            _equal(first, second)
    else:
        assert actual == expected


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, _native_copy])
def test_copy_preserves_lazy_shape_without_interchange(analysis, copier, monkeypatch):
    import molsysmt.native.interactions_dict as codec
    from molsysmt.interactions._frame_validity import _FrameFilteredInteractions

    def forbidden(*args, **kwargs):
        pytest.fail("Copying crossed a constructor, packing or interchange boundary")

    before = vars(analysis).copy()
    with monkeypatch.context() as patch:
        patch.setattr(codec, "_encode_interactions", forbidden)
        patch.setattr(codec, "_decode_interactions", forbidden)
        patch.setattr(msm.Interactions, "__init__", forbidden)
        patch.setattr(msm.Interactions, "remap", forbidden)
        patch.setattr(_FrameFilteredInteractions, "_packed", forbidden)
        if hasattr(analysis, "_segments"):
            patch.setattr(type(analysis), "_packed", forbidden)
        duplicate = copier(analysis)
    assert type(duplicate) is type(analysis)
    assert duplicate is not analysis
    assert vars(analysis).keys() == before.keys()
    assert all(vars(analysis)[key] is value for key, value in before.items())
    if "_packed_result" in before:
        assert duplicate._packed_result is None
    if "_root" in before:
        assert duplicate._root is not analysis._root
    if "_segments" in before:
        assert all(
            first[0] is not second[0]
            for first, second in zip(duplicate._segments, analysis._segments)
        )
    _equal(duplicate.to_dict(), analysis.to_dict())
    _equal(
        duplicate.query(structure_indices=[3, 1, 0, 4, 3]).to_dict(),
        analysis.query(structure_indices=[3, 1, 0, 4, 3]).to_dict(),
    )
    assert duplicate.query(structure_indices=[1]).n_interactions == 0
    assert (
        duplicate.query(structure_indices=[4])
        .to_dict()["evaluated_structure_indices"]
        .size
        == 0
    )


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, _native_copy])
def test_copy_detaches_metadata_and_validity(analysis, copier):
    duplicate = copier(analysis)
    duplicate.parameters["cutoff"]["value"] = 0.8
    duplicate.software["producer"] = "different"
    duplicate.measure_units["distance"] = "angstrom"
    duplicate._execution_records[0][1]["chunk_size"] = 9
    assert analysis.parameters["cutoff"]["value"] == 0.5
    assert analysis.software == {"producer": "0.1"}
    assert analysis.measure_units == {"distance": "nm"}
    assert analysis._execution_records[0][1]["chunk_size"] == 2
    # Invalidation applies to full logical analyses, not occurrence selections.
    if analysis._is_full:
        changed = duplicate.invalidate_structures([3])
        assert 3 not in changed.evaluated_structure_indices
        assert 3 in analysis.evaluated_structure_indices


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, _native_copy])
def test_copy_shares_only_immutable_bytes_with_independent_headers(analysis, copier):
    duplicate = copier(analysis)
    original = analysis.atom_source_indices
    detached = duplicate.atom_source_indices
    assert original is not detached
    assert np.shares_memory(original, detached)
    with pytest.raises(ValueError):
        detached.flags.writeable = True
    detached.shape = (2, 3)
    assert original.shape == (6,)
    # Selected positions may be mutable arrays: their payload must be detached.
    if "_positions" in vars(analysis):
        duplicate._positions.shape = (duplicate._positions.size, 1)
        assert analysis._positions.ndim == 1


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, _native_copy])
def test_copy_does_not_trust_readonly_flags_or_share_query_indexes(copier):
    source = _analysis()
    source.query(atom_indices=[0])
    writable = np.arange(3)
    readonly_alias = writable.view()
    readonly_alias.flags.writeable = False
    source.application = {"readonly_alias": readonly_alias, "writable": writable}
    duplicate = copier(source)
    for name in (
        "_atom_relation_ids",
        "_atom_relation_offsets",
        "_relation_occurrence_ids",
        "_relation_occurrence_offsets",
    ):
        assert not np.shares_memory(getattr(duplicate, name), getattr(source, name))
    writable[:] = 99
    np.testing.assert_array_equal(duplicate.application["readonly_alias"], [0, 1, 2])
    duplicate.application["writable"][:] = 42
    np.testing.assert_array_equal(writable, [99, 99, 99])


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, _native_copy])
def test_copy_keeps_cycles_aliases_proxy_metadata_and_subclass_slots(copier):
    class Extended(msm.Interactions):
        __slots__ = ("extra", "__private")

        def __init__(self):
            pytest.fail("Copying must not call an extension constructor")

    source = object.__new__(Extended)
    source.__dict__.update(vars(_analysis()))
    source.extra = source.parameters
    source._Extended__private = source
    source.application = {"self": source, "parameters": source.parameters}
    proxy_data = {"parameters": source.parameters}
    proxy = MappingProxyType(proxy_data)
    proxy_data["self"] = proxy
    source.application["proxy"] = proxy
    source.application["proxy_alias"] = proxy
    duplicate = copier(source)
    assert type(duplicate) is Extended
    assert duplicate.extra is duplicate.parameters
    assert duplicate._Extended__private is duplicate
    assert duplicate.application["self"] is duplicate
    assert duplicate.application["parameters"] is duplicate.parameters
    new_proxy = duplicate.application["proxy"]
    assert new_proxy is duplicate.application["proxy_alias"]
    assert new_proxy["self"] is new_proxy
    assert new_proxy["parameters"] is duplicate.parameters
    duplicate.extra["cutoff"]["value"] = 0.7
    assert source.extra["cutoff"]["value"] == 0.5


def test_enclosing_deepcopy_preserves_graph_memo(analysis):
    envelope = {
        "analysis": analysis,
        "again": analysis,
        "metadata": analysis.parameters,
    }
    envelope["self"] = envelope
    duplicate = copy.deepcopy(envelope)
    assert duplicate["self"] is duplicate
    assert duplicate["analysis"] is duplicate["again"]
    assert duplicate["metadata"] is duplicate["analysis"].parameters
    assert duplicate["metadata"] is not analysis.parameters


def test_graph_copy_preserves_column_alias_when_analysis_is_copied_first():
    source = _analysis()
    duplicate, column = copy.deepcopy([source, source.participant_atoms])
    assert duplicate.participant_atoms is column
    with pytest.raises(ValueError):
        column.flags.writeable = True


def test_graph_copy_rejects_mutable_array_already_in_memo():
    source = _analysis()
    original = source.participant_atoms.copy()
    with pytest.raises(TypeError, match="copy the analysis before its raw arrays"):
        copy.deepcopy([source.participant_atoms, source])
    np.testing.assert_array_equal(source.participant_atoms, original)
    with pytest.raises(ValueError):
        source.participant_atoms.flags.writeable = True


@pytest.mark.parametrize("invalid", [None, 1, "True", np.bool_(True)])
def test_native_copy_validates_its_public_boundary(invalid):
    from molsysmt._private.smonitor import ArgumentError

    source = _analysis()
    with pytest.raises(ArgumentError):
        source.copy(skip_digestion=invalid)


def test_native_copy_accepts_explicit_trusted_delegation():
    source = _analysis()
    duplicate = source.copy(skip_digestion=True)
    assert duplicate is not source
    _equal(duplicate.to_dict(), source.to_dict())


@pytest.mark.parametrize("kind", ["filtered", "patched"])
def test_copy_preserves_existing_packed_cache_without_aliasing(kind):
    source = _analysis()
    source = (
        source.invalidate_structures([0])
        if kind == "filtered"
        else source.replace_structures(_analysis([], coverage=[0]))
    )
    source.measurements
    packed = source._packed_result
    duplicate = copy.deepcopy(source)
    assert source._packed_result is packed
    assert duplicate._packed_result is not packed
    _equal(duplicate.to_dict(), source.to_dict())
    duplicate._packed_result.parameters["cutoff"]["value"] = 1.0
    assert packed.parameters["cutoff"]["value"] == 0.5


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, _native_copy])
def test_copied_analysis_roundtrip_preserves_parallel_identity_and_images(
    tmp_path, copier
):
    source = _analysis()
    duplicate = copier(source)
    path = tmp_path / "copied.h5msm"
    with msm.pyunitwizard.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        msm.h5msm.write_layers(path, interactions={"analysis": duplicate})
        restored = msm.h5msm.read(path).interactions["analysis"]
    _equal(restored.to_dict(), source.to_dict())
    selected = restored.query(structure_indices=[3, 1, 0]).to_dict()
    assert selected["occurrence_indices"].tolist() == [2, 0, 1]


def test_copy_retains_immutable_occurrence_measurement_and_periodic_payloads():
    source = _analysis()
    duplicate = source.copy()
    for original, detached in [
        (source.participant_atoms, duplicate.participant_atoms),
        (source.occurrence_relations, duplicate.occurrence_relations),
        (source.occurrence_structures, duplicate.occurrence_structures),
        (source.image_vectors, duplicate.image_vectors),
        (source.measurements["distance"], duplicate.measurements["distance"]),
        (source.evaluated_structure_indices, duplicate.evaluated_structure_indices),
    ]:
        assert detached is not original
        assert np.shares_memory(detached, original)
        with pytest.raises(ValueError):
            detached.flags.writeable = True
    duplicate.measurements["distance"].shape = (3, 1)
    assert source.measurements["distance"].shape == (3,)


def test_querying_copy_does_not_build_source_reverse_indexes(analysis):
    def residents(value):
        yield value
        if "_root" in vars(value):
            yield value._root
        for segment in vars(value).get("_segments", ()):
            yield segment[0]

    sources = list(residents(analysis))
    before = [vars(value).copy() for value in sources]
    duplicate = analysis.copy()
    duplicate.query(atom_indices=[0], structure_indices=[3, 0])
    for source, snapshot in zip(sources, before):
        assert vars(source).keys() == snapshot.keys()
        assert all(vars(source)[key] is value for key, value in snapshot.items())
