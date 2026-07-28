# Installation

MolSysMT is distributed through the 'uibcdf' conda channel.
If there is no reason to install the library from the source code, we highly recommend working with
conda.

```bash
conda install -c uibcdf molsysmt
```

:::{admonition} Precompiled native kernels
MolSysMT's numerical kernels are compiled into the installed Rust extension, so
there is no first-use JIT compilation or kernel warm-up step.
:::
