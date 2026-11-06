"""Protect process-global configuration writer serialization and restoration."""

from concurrent.futures import ThreadPoolExecutor
from threading import Event

import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt.configure import with_configure_overrides
from molsysmt.native import Structures


def _snapshot():
    return tuple(
        getattr(msm.configure, name)
        for name in ("gpu_mode", "use_gpu", "gpu_backend", "precision", "cell_list")
    )


@pytest.fixture(autouse=True)
def restore_configuration():
    names = tuple(vars(msm.configure))
    values = {
        name: getattr(msm.configure, name)
        for name in (
            "gpu_mode",
            "use_gpu",
            "gpu_backend",
            "precision",
            "cell_list",
            "chunk_size",
            "parallel_mode",
            "num_threads",
        )
    }
    yield
    for name, value in values.items():
        setattr(msm.configure, name, value)
    if "not_configuration" not in names and hasattr(msm.configure, "not_configuration"):
        delattr(msm.configure, "not_configuration")


@pytest.mark.parametrize(
    "factory", [msm.configure.context, msm.configure.configure_context]
)
@pytest.mark.parametrize(
    "name", ["not_configuration", "_debugging", "context", "logging_setup"]
)
def test_context_refuses_invalid_names_before_any_write(factory, name):
    before = dict(vars(msm.configure))
    with pytest.raises((msm.ArgumentError, UnknownArgumentError)):
        with factory(chunk_size=3, **{name: False}):
            pytest.fail("Invalid configuration was published.")
    assert vars(msm.configure).keys() == before.keys()
    for key, value in before.items():
        assert vars(msm.configure)[key] is value


@pytest.mark.parametrize(
    "factory", [msm.configure.context, msm.configure.configure_context]
)
def test_context_refuses_conflicting_gpu_aliases_atomically(factory):
    before = _snapshot()
    with pytest.raises(msm.ArgumentConflictError):
        with factory(gpu_mode=True, use_gpu=False, precision="single"):
            pytest.fail("Contradictory aliases were published.")
    assert _snapshot() == before


def test_nested_reused_context_restores_values_after_exceptions():
    before = _snapshot()
    repeated = msm.configure.context(use_gpu=False, precision="single")
    with pytest.raises(RuntimeError, match="deliberate"):
        with repeated:
            with repeated:
                assert msm.configure.gpu_mode is False
            assert msm.configure.gpu_mode is False
            with msm.configure.context(gpu_mode=True, precision="double"):
                assert msm.configure.use_gpu is True
                assert msm.configure.precision == "double"
            assert msm.configure.precision == "single"
            raise RuntimeError("deliberate")
    assert _snapshot() == before
    with repeated:
        assert msm.configure.gpu_mode is False
    assert _snapshot() == before


def test_overlapping_decorated_calls_serialize_every_global_override():
    before = _snapshot()
    first_entered, second_attempted, second_entered = Event(), Event(), Event()
    release_first, first_finished = Event(), Event()

    @with_configure_overrides
    def probe(
        use_gpu=None,
        gpu_backend=None,
        precision=None,
        cell_list=None,
        parallel=None,
        num_threads=None,
    ):
        if use_gpu is False:
            first_entered.set()
            assert release_first.wait(5)
        else:
            second_entered.set()
            assert first_finished.wait(5)
        return _snapshot(), msm.configure._get_effective_num_threads(10)

    def first():
        try:
            return probe(
                use_gpu=False,
                gpu_backend="first-marker",
                precision="single",
                cell_list=False,
                parallel=False,
                num_threads=1,
            )
        finally:
            first_finished.set()

    def second():
        assert first_entered.wait(5)
        second_attempted.set()
        return probe(
            use_gpu=True,
            gpu_backend="second-marker",
            precision="double",
            cell_list=True,
            parallel=True,
            num_threads=2,
        )

    with ThreadPoolExecutor(max_workers=2) as pool:
        a, b = pool.submit(first), pool.submit(second)
        try:
            assert first_entered.wait(5) and second_attempted.wait(5)
            entered_while_first_active = second_entered.wait(0.2)
        finally:
            release_first.set()
        first_result, second_result = a.result(timeout=5), b.result(timeout=5)
    assert not entered_while_first_active
    assert first_result == ((False, False, "first-marker", "single", False), 1)
    assert second_result == ((True, True, "second-marker", "double", True), 2)
    assert _snapshot() == before


def test_no_global_override_public_call_does_not_wait_for_a_context_writer():
    entered, release = Event(), Event()
    before = _snapshot()
    source = Structures(
        coordinates=msm.pyunitwizard.quantity([[[0, 0, 0], [1, 0, 0]]], "nm")
    )

    def hold():
        with msm.configure.context(cell_list=False):
            entered.set()
            assert release.wait(5)

    with ThreadPoolExecutor(max_workers=2) as pool:
        writer = pool.submit(hold)
        assert entered.wait(5)
        try:
            # The accepted process-global contract permits this observation.
            assert msm.configure.cell_list is False
            call = pool.submit(
                msm.structure.get_distances, source, pbc=False, parallel=False
            )
            result = call.result(timeout=2)
        finally:
            release.set()
            writer.result(timeout=5)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="nm"), [[[0, 1], [1, 0]]]
    )
    assert _snapshot() == before


def test_public_geometry_call_restores_global_aliases_when_kernel_raises(monkeypatch):
    from molsysmt._private import rust_backend

    before = _snapshot()
    source = Structures(
        coordinates=msm.pyunitwizard.quantity([[[0, 0, 0], [1, 0, 0]]], "nm")
    )

    def fail(*args, **kwargs):
        assert msm.configure.gpu_mode is False and msm.configure.use_gpu is False
        raise RuntimeError("deliberate kernel failure")

    monkeypatch.setattr(rust_backend, "get_distances_single_system", fail)
    with pytest.raises(RuntimeError, match="deliberate kernel failure"):
        msm.structure.get_distances(source, pbc=False, use_gpu=False, parallel=False)
    assert _snapshot() == before


@pytest.mark.parametrize(
    "factory", [msm.configure.context, msm.configure.configure_context]
)
@pytest.mark.parametrize("skip", [False, True])
def test_trusted_skip_retains_key_and_alias_integrity(factory, skip):
    with pytest.raises((msm.ArgumentError, UnknownArgumentError)):
        with factory(not_configuration=1, skip_digestion=skip):
            pytest.fail("Trusted delegation created configuration data.")
    with pytest.raises(msm.ArgumentConflictError):
        with factory(gpu_mode=False, use_gpu=True, skip_digestion=skip):
            pytest.fail("Trusted delegation published contradictory aliases.")


def test_decorated_call_refuses_conflicting_aliases_before_body():
    @with_configure_overrides
    def probe(use_gpu=None, gpu_mode=None):
        pytest.fail("A conflicting call reached its implementation.")

    before = _snapshot()
    with pytest.raises(msm.ArgumentConflictError):
        probe(use_gpu=True, gpu_mode=False)
    assert _snapshot() == before


def test_session_setter_waits_for_context_and_keeps_its_persistent_update():
    entered, release, attempted, finished = Event(), Event(), Event(), Event()

    def hold():
        with msm.configure.context(parallel_mode=False, num_threads=7):
            entered.set()
            assert release.wait(5)

    def update():
        attempted.set()
        msm.configure.set_parallelization(parallel=True, num_threads=2)
        finished.set()

    with ThreadPoolExecutor(max_workers=2) as pool:
        writer = pool.submit(hold)
        assert entered.wait(5)
        setter = pool.submit(update)
        try:
            assert attempted.wait(5)
            finished_before_context_exit = finished.wait(0.2)
        finally:
            release.set()
        writer.result(timeout=5)
        setter.result(timeout=5)
    assert not finished_before_context_exit
    assert msm.configure.parallel_mode is True
    assert msm.configure.get_num_threads() == 2
