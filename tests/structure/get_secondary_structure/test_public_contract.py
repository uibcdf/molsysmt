"""Secondary-structure projections retain source groups and full backbone context."""

import inspect

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(scope="module")
def source():
    return msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        structure_indices=[0, 8, 2],
    )


@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("selection", [[3, 1, 3], np.array([3, 1, 3])])
def test_explicit_group_order_repetitions_and_structure_axes(source, selection, syntax):
    whole = msm.structure.get_secondary_structure(source, simplified=False)
    actual = msm.structure.get_secondary_structure(
        source,
        selection=selection,
        structure_indices=[2, 0, 2],
        simplified=False,
        syntax=syntax,
    )
    assert actual.shape == (3, 3)
    assert actual.dtype == np.dtype("U2")
    np.testing.assert_array_equal(actual, whole[[2, 0, 2]][:, [3, 1, 3]])


def test_public_signature_declares_validation_and_execution_controls():
    parameters = inspect.signature(msm.structure.get_secondary_structure).parameters
    assert "skip_digestion" in parameters
    assert "heavy_mode" in parameters


@pytest.mark.parametrize("simplified", [False, True])
@pytest.mark.parametrize("units", ["nm", "pm"])
def test_full_context_backend_parity_units_and_source_preservation(
    source, simplified, units
):
    import mdtraj as md

    expected = md.compute_dssp(
        msm.convert(source, to_form="mdtraj.Trajectory"), simplified=simplified
    )
    before = msm.pyunitwizard.get_value(source.structures.coordinates).copy()
    with msm.pyunitwizard.context(
        standard_units=[units, "ps", "Da", "K", "e", "radians"]
    ):
        actual = msm.structure.get_secondary_structure(
            source, selection=[4, 0, 2], simplified=simplified
        )
    np.testing.assert_array_equal(actual, expected[:, [4, 0, 2]])
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates), before
    )
    assert not np.shares_memory(actual, expected)


@pytest.mark.parametrize(
    "groups,frames,shape",
    [([], [2, 0], (2, 0)), ([3, 1, 3], [], (0, 3)), ([], [], (0, 0))],
)
def test_empty_axes_are_typed_and_do_not_compute(
    source, groups, frames, shape, monkeypatch
):
    import mdtraj as md

    def forbidden(*args, **kwargs):
        pytest.fail("Empty axes must not execute DSSP")

    monkeypatch.setattr(md, "compute_dssp", forbidden)
    result = msm.structure.get_secondary_structure(
        source, selection=groups, structure_indices=frames
    )
    assert result.shape == shape and result.dtype == np.dtype("U2")


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(selection=[-1]),
        dict(selection=[99]),
        dict(structure_indices=[-1]),
        dict(structure_indices=[99]),
        dict(simplified="yes"),
        dict(skip_digestion="yes"),
        dict(heavy_mode="all"),
    ],
)
def test_invalid_arguments_refuse_before_backend(source, kwargs, monkeypatch):
    import mdtraj as md

    from molsysmt._private.smonitor import ArgumentError

    def forbidden(*args, **kw):
        pytest.fail("Invalid inputs must not reach DSSP")

    monkeypatch.setattr(md, "compute_dssp", forbidden)
    with pytest.raises((ArgumentError, TypeError)):
        msm.structure.get_secondary_structure(source, **kwargs)


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "mdtraj.Trajectory", "file:h5msm"])
def test_supported_forms_and_chunked_native_file_queries(source, form, tmp_path):
    if form == "file:h5msm":
        path = tmp_path / "source.h5msm"
        msm.convert(source, to_form=str(path))
        system = str(path)
    else:
        system = msm.convert(source, to_form=form)
    expected = msm.structure.get_secondary_structure(
        source, selection=[4, 0, 2], structure_indices=[2, 0, 2], simplified=False
    )
    # Foreign MDTraj has no registered heavy-support promise; eager still uses
    # its registered iterator. Native/file forms exercise forced single chunks.
    mode = "off" if form == "mdtraj.Trajectory" else "force"
    with msm.configure.context(chunk_size=1):
        result = msm.structure.get_secondary_structure(
            system,
            selection=[4, 0, 2],
            structure_indices=[2, 0, 2],
            simplified=False,
            heavy_mode=mode,
        )
    np.testing.assert_array_equal(result, expected)


def test_numerical_budget_refuses_before_context_conversion(source, monkeypatch):
    monkeypatch.setattr(msm.configure, "max_ram_usage", 8)
    with pytest.raises(msm.MemoryBudgetExceededError, match="DSSP labels"):
        msm.structure.get_secondary_structure(source)


def test_optional_attribution_credits_the_executed_method_and_version(source):
    import mdtraj as md

    ackredit = pytest.importorskip("ackredit")

    with ackredit.session("DSSP provider contract"):
        first = msm.structure.get_secondary_structure(source, selection=[3, 1, 3])
        second = msm.structure.get_secondary_structure(source, selection=[3, 1, 3])
        ids = set(ackredit.get_used_items())
        assert {
            "doi:10.1002/bip.360221211",
            "doi:10.1016/j.bpj.2015.08.015",
            f"software:mdtraj:{md.__version__}",
        } <= ids
    np.testing.assert_array_equal(first, second)
    assert not np.shares_memory(first, second)


@pytest.mark.parametrize("skip", [False, True])
def test_missing_mdtraj_has_host_diagnostic_before_import(source, monkeypatch, skip):
    from depdigest import is_installed
    from depdigest.core import checker

    from molsysmt._private.smonitor import LibraryNotFoundError

    original = checker.find_spec

    def absent(name, *args, **kwargs):
        return None if name == "mdtraj" else original(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", absent)
        is_installed.cache_clear()
        with pytest.raises(LibraryNotFoundError, match="(?i)mdtraj"):
            msm.structure.get_secondary_structure(source, skip_digestion=skip)
    finally:
        is_installed.cache_clear()


def test_auto_chunk_admission_matches_eager_and_eager_refusal(source, monkeypatch):
    import mdtraj as md

    expected = msm.structure.get_secondary_structure(
        source, structure_indices=[2, 0, 2]
    )
    original = md.compute_dssp
    counts = []

    def observe(trajectory, **kwargs):
        counts.append(trajectory.n_frames)
        return original(trajectory, **kwargs)

    monkeypatch.setattr(md, "compute_dssp", observe)
    with msm.configure.context(max_ram_usage=10240, chunk_size=1):
        result = msm.structure.get_secondary_structure(
            source, structure_indices=[2, 0, 2]
        )
        assert counts == [1, 1, 1]
        with pytest.raises(msm.MemoryBudgetExceededError):
            msm.structure.get_secondary_structure(
                source, structure_indices=[2, 0, 2], heavy_mode="off"
            )
    np.testing.assert_array_equal(result, expected)


def test_optional_attribution_absence_preserves_labels(source, monkeypatch):
    from molsysmt import _ackredit

    expected = msm.structure.get_secondary_structure(source)
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    np.testing.assert_array_equal(
        msm.structure.get_secondary_structure(source), expected
    )
