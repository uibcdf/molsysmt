# Installation

MolSysMT is distributed through the 'uibcdf' conda channel.
If there is no reason to install the library from the source code, we highly recommend working with
conda.

```bash
conda install -c uibcdf molsysmt
```

## Using Jupyter notebooks

For molecular visualization with MolSysViewer in Jupyter, use
`ipykernel>=7.4.0` in the environment that runs your notebook kernel:

```bash
conda install -c conda-forge "ipykernel>=7.4.0" jupyterlab
```

The selected notebook kernel can use a different environment from the Jupyter
server. Check the kernel's version with `import ipykernel; ipykernel.__version__`
and restart it after an upgrade. Version 7.4.0 includes a
[shell-message transport correction](https://github.com/ipython/ipykernel/pull/1529)
that prevents a demonstrated cause of stalled notebook execution.

This is a notebook-host requirement. Headless molecular calculations do not
require Jupyter or ipykernel.
