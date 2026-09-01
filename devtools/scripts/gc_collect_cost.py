"""Benchmark public structure calls formerly dominated by full GC collection."""

from __future__ import annotations

from statistics import median
from time import perf_counter
from typing import Callable

import molsysmt as msm


def _median_call_time(operation: Callable[[], object], repeats: int = 15) -> float:
    operation()
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        operation()
        samples.append(perf_counter() - start)
    return median(samples)


def main() -> None:
    molecular_system = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        to_form="molsysmt.MolSys",
    )
    operations = {
        "get_center": lambda: msm.structure.get_center(molecular_system),
        "get_radius_of_gyration": lambda: msm.structure.get_radius_of_gyration(
            molecular_system
        ),
        "get_principal_axes": lambda: msm.structure.get_principal_axes(molecular_system),
        "get_contacts": lambda: msm.structure.get_contacts(
            molecular_system,
            selection="atom_name=='CA'",
            threshold="0.8 nm",
        ),
    }

    print("function                         median")
    for name, operation in operations.items():
        elapsed = _median_call_time(operation)
        print(f"{name:<30} {elapsed * 1000:8.2f} ms")


if __name__ == "__main__":
    main()
