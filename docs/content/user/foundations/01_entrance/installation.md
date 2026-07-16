# Installation

MolSysMT is distributed through the 'uibcdf' conda channel.
If there is no reason to install the library from the source code, we highly recommend working with
conda.

```bash
conda install -c uibcdf molsysmt
```

:::{admonition} First-use Numba compilation
Some MolSysMT kernels are accelerated with Numba. The first call to those
kernels can take a moment while they compile. To avoid that latency, run
`molsysmt.warmup()` once after installing. For an auditable environment check,
use `molsysmt.warmup(strict=True, return_report=True)` and inspect the returned
report.
:::
