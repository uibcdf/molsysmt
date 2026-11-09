"""Receive native policy serialization across independent real Views (#613)."""

from concurrent.futures import ThreadPoolExecutor
from threading import Event

import molsysviewer as msv
import numpy as np

import molsysmt as msm


def test_two_view_context_writers_and_explicit_cpu_reads_preserve_each_owner():
    names = ("gpu_mode", "use_gpu", "precision", "parallel_mode", "num_threads")
    initial = tuple(getattr(msm.configure, name) for name in names)
    entered, attempted, second_entered, release = (Event() for _ in range(4))
    with msv.demo["pentalanine"] as seed:
        with seed.extract(structure_indices=[0, 8, 3]) as first:
            with seed.extract(structure_indices=[8, 3]) as second:
                views, frames = (first, second), ([2, 0], [1, 0])
                coordinates = [
                    msm.pyunitwizard.get_value(
                        msm.get(view.molsys, coordinates=True), to_unit="nm"
                    ).copy()
                    for view in views
                ]
                states = [view.export_state() for view in views]
                statuses = [view.addons.molsysmt.get_sync_status() for view in views]

                def calculate(index):
                    result = views[index].addons.molsysmt.structure.get_distances(
                        selection=[0, 4],
                        selection_2=[1, 5],
                        structure_indices=frames[index],
                        pbc=False,
                        use_gpu=False,
                        parallel=False,
                        num_threads=1,
                    )
                    raw = coordinates[index][frames[index]]
                    delta = raw[:, [0, 4], None, :] - raw[:, None, [1, 5], :]
                    np.testing.assert_allclose(
                        msm.pyunitwizard.get_value(result, to_unit="nm"),
                        np.sqrt(np.sum(delta**2, axis=-1)),
                        atol=1e-12,
                    )

                def one():
                    with msm.configure.context(use_gpu=False, num_threads=1):
                        entered.set()
                        calculate(0)
                        assert release.wait(10)
                        assert msm.configure.gpu_mode is False

                def two():
                    assert entered.wait(10)
                    attempted.set()
                    with msm.configure.context(use_gpu=True, num_threads=1):
                        second_entered.set()
                        calculate(1)
                        assert msm.configure.gpu_mode is True

                with ThreadPoolExecutor(max_workers=2) as pool:
                    a, b = pool.submit(one), pool.submit(two)
                    try:
                        assert entered.wait(10) and attempted.wait(10)
                        crossed = second_entered.wait(0.2)
                    finally:
                        release.set()
                    a.result(timeout=10)
                    b.result(timeout=10)
                assert not crossed and second_entered.is_set()
                assert tuple(getattr(msm.configure, name) for name in names) == initial
                for index, view in enumerate(views):
                    np.testing.assert_array_equal(
                        msm.pyunitwizard.get_value(
                            msm.get(view.molsys, coordinates=True), to_unit="nm"
                        ),
                        coordinates[index],
                    )
                    assert view.export_state() == states[index]
                    assert view.addons.molsysmt.get_sync_status() == statuses[index]
