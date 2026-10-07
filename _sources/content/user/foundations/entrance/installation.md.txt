(user-foundations-entrance-installation)=
# Installation

MolSysMT supports Python **3.13** (recommended), **3.12**, and **3.11**. High-performance compute kernels ship precompiled natively within the package.

---

## Official Installation

The official distribution channel for MolSysMT is maintained under the [**`uibcdf`** Conda channel](https://anaconda.org/channels/uibcdf). We strongly recommend installing MolSysMT within a dedicated Conda/Mamba environment:

```bash
conda install -c uibcdf -c conda-forge molsysmt
```

Or using `mamba`:

```bash
mamba install -c uibcdf -c conda-forge molsysmt
```

---

## Development Version from Source

To test the latest features or contribute to the library, you can install the development version directly from the source repository on GitHub.

### 1. Clone the Repository
```bash
git clone https://github.com/uibcdf/molsysmt.git
cd molsysmt
```

### 2. Create the Development Conda Environment
Use the provided environment specification file located at `devtools/conda-envs/development_env.yaml` to create an isolated environment with Python 3.13 and all development dependencies:

```bash
conda env create -n molsysmt-dev -f devtools/conda-envs/development_env.yaml
```

### 3. Activate the Environment and Install in Editable Mode
Activate the newly created environment and install MolSysMT in editable mode without pulling redundant dependencies:

```bash
conda activate molsysmt-dev
pip install --no-deps --editable .
```

---

:::{admonition} Precompiled Native Kernels
:class: note
MolSysMT's high-performance analytical kernels (distances, RMSD, SASA, gyration radius, dihedrals) are precompiled in Rust and integrated directly into the binary extension module.
:::
