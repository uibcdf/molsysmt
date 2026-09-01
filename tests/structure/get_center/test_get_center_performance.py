"""Performance regression tests for the public center calculation."""

from statistics import median
from time import perf_counter

import molsysmt as msm


def test_get_center_small_system_stays_below_public_call_budget():
    molecular_system = msm.convert(
        msm.systems["particles 4"]["traj_particles_4.xyznpy"],
        to_form="XYZ",
    )

    msm.structure.get_center(molecular_system)

    iterations = 10
    samples = []
    for _ in range(5):
        start = perf_counter()
        for _ in range(iterations):
            msm.structure.get_center(molecular_system)
        samples.append((perf_counter() - start) / iterations)

    assert median(samples) < 0.050
