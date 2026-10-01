"""Measure optional workflow tracking alongside identical result bibliography.

Run in an environment with Ackredit and RDKit installed. No report files or DOI
lookups are requested. This small calculation measures fixed per-call costs;
it does not predict large-trajectory throughput or measure a pre-attribution
release. Both modes still construct the same portable result bibliography.
"""

import argparse
import json
import platform
from statistics import median
from time import perf_counter
from unittest.mock import patch

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=100)
    parser.add_argument("--structures", type=int, default=3)
    options = parser.parse_args()
    if options.repetitions < 1 or options.structures < 1:
        parser.error("repetitions and structures must be positive")

    import ackredit
    from rdkit import Chem

    import molsysmt as msm
    from molsysmt import _ackredit

    molsys = msm.convert(Chem.AddHs(Chem.MolFromSmiles("O.O")), to_form="molsysmt.MolSys")
    xyz = np.array([[0, 0, 0], [.28, 0, 0], [.1, 0, 0], [0, .1, 0], [.28, .1, 0], [.28, 0, .1]])
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(
        np.repeat(xyz[None], options.structures, axis=0), "nm"))

    def calculate():
        return msm.interactions.hbonds.get_hbonds(molsys, pbc=False)

    real_backend = _ackredit.backend
    # Warm chemistry, dependency introspection and the existing numerical kernels.
    calculate()
    times = {"without_provider": [], "with_provider": []}
    with ackredit.session("attribution-benchmark"):
        for _ in range(options.repetitions):
            # Alternate order to avoid assigning all warm-up/drift to one mode.
            order = list(times) if _ % 2 == 0 else list(reversed(times))
            for mode in order:
                backend = real_backend if mode == "with_provider" else lambda: None
                with patch.object(_ackredit, "backend", backend):
                    start = perf_counter()
                    result = calculate()
                    times[mode].append((perf_counter() - start) * 1000)
                assert result.n_interactions == options.structures
        used_items = len(ackredit.get_used_items())
    medians = {mode: median(values) for mode, values in times.items()}
    print(json.dumps(dict(
        python=platform.python_version(), platform=platform.platform(),
        molsysmt=msm.__version__, ackredit=ackredit.__version__,
        repetitions=options.repetitions, atoms=6, structures=options.structures,
        median_ms=medians, provider_delta_ms=medians["with_provider"] - medians["without_provider"],
        bibliography_bytes=len(json.dumps(result.parameters["attribution"]).encode()),
        workflow_items=used_items,
        limitations="Both modes retain bibliography; fixed-call fixture, no large-trajectory claim.",
    ), indent=2))


if __name__ == "__main__":
    main()
