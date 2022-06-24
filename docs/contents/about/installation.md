# Installation

MolSysMT is distributed through the 'uibcdf' conda channel.
If there is no reason to install the library from the source code, we highly recommend working with
conda.

## Production version

If you want to work with the last production version:

```bash
conda install -c uibcdf molsysmt
```

## Developing version

### Get the code

The raw code fully alive can be cloned from the [github repository](https://github.com/uibcdf/MolSysMT) as follows:

```bash
git clone https://github.com/uibcdf/MolSysMT.git
```

or with the native GitHub cli:

```bash
git repo clone uibcdf/MolSysMT
```

If you are going to contribute to the code, having a look to the Developer Guide is strongly suggested. 

### Work with a conda environment

Instructions to build a conda environment depending on the case. Description of the required
packages.

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

- [ParmEd](https://parmed.github.io/ParmEd/)
- [MDAnalysis](https://www.mdanalysis.org/)
- [pytraj](https://amber-md.github.io/pytraj/latest/index.html)
- [Modeller](https://salilab.org/modeller/)
- [Biopython](https://biopython.org/)
- [OpenExplorer (dev)](https://www.uibcdf.org/OpenExplorer)
- [OpenMolecularSystems (dev)](https://www.uibcdf.org/OpenMolecularSystem)

### Install from the source code

Having the dependencies solved, the command to install MolSysMT from its source code is:

```bash
cd MolSysMT
python setup.py develop
```

