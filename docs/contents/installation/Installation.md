# Installation

MolSysMT is distributed in its stable and testing version through a the 'uibcdf' conda channel.
If there is no reason to install the library from the source code, we highly recommend working with
conda.

## Last stable version

There is no stable version yet

## Last testing version

If you want to work with the last testing version:

```bash
conda install -c uibcdf/label/dev molsysmt
```

To uninstall this library:

```bash
conda remove pyunitwizard
```

## Developing version from the source code

### The source code

The raw code fully alive can be cloned from the [github repository](https://github.com/uibcdf/MolSysMT) as follows:

```bash
git clone https://github.com/uibcdf/MolSysMT.git
```

### A conda environment

This step is not required, but it is recomended. You can use a python packages and virtual
environments manager, as conda. If this is the case, use MolSysMT in a python 3.7 environment. You
can create a new one this way (where `ENV_NAME` is the name you want to give to the new
environment):

```bash
conda create --name ENV_NAME python=3.7
```

Load the virtual environment where MolSysMT is going to be installed. If you just create a new
environment with conda:

```bash
conda activate ENV_NAME
```

### Dependencies

Unlike the installation process with the testing and stable versions, in this case the dependencies have to be solved manually
before going to the next step. This is the list of packages you have to have in your OS or your
python environment:

- [gfortran](https://gcc.gnu.org/) (or any other fortran compiler)
- [python = 3.7](https://www.python.org/)
- [mmtf-python](https://mmtf.rcsb.org/index.html)
- [Pandas](https://pandas.pydata.org/)
- [NetworkX](https://networkx.org/)
- [OpenMM](http://openmm.org/)
- [PDBFixer](https://github.com/openmm/pdbfixer)
- [MDTraj](http://mdtraj.org/)
- [NGLView](http://nglviewer.org/nglview/latest/)
- [PyUnitWizard >= 0.2.0 (dev)](https://www.uibcdf.org/PyUnitWizard)
- [AmberTools](http://ambermd.org/AmberTools.php)

If you are working in a conda environment, find here the installation commands to solve this
dependencies:

```bash
conda install mmtf-python pandas networkx openmm pdbfixer nglview ambertools mdtraj
conda install -c uibcdf/label/dev pyunitwizard
```

There is also a set of optional libraries you may want to install depending on how you are going to use
MolSysMT:

- [ParmEd](https://parmed.github.io/ParmEd/)
- [MDAnalysis](https://www.mdanalysis.org/)
- [pytraj](https://amber-md.github.io/pytraj/latest/index.html)
- [Modeller](https://salilab.org/modeller/)
- [Biopython](https://biopython.org/)
- [OpenExplorer (dev)](https://www.uibcdf.org/OpenExplorer)
- [OpenMolecularSystems (dev)](https://www.uibcdf.org/OpenMolecularSystem)

If you want to install this optional libraries in your conda environment, go with the following
command:

```bash
conda install parmed mdanalysis pytraj biopython
```

### Additional dependencies for developers

If you are going to contribute to develope or document MolSysMT, you will need these other
packages:

```bash
conda install jupyterlab
conda install sphinx 
```

### Installation from the source code

Having the dependencies solved, the command to install MolSysMT from its source code is:

```bash
cd MolSysMT
python setup.py develop
```

#### Patching NGLView

The methods to load `molsysm.MolSys` objects with NGLview has not being implemented yet this
visualization library. However, the patch is included in MolSysMT. To apply it, you only need to
execute once in you environment the following lines (with python, ipython or jupyter):

```python
In [1]: from molsysmt.tools.nglview import adding_molsysmt

In [2]: adding_molsysmt()
```

### Uninstallation

If you want to uninstall the developing version of MolSysMT, do the following:

```bash
pip uninstall molsysmt
```

