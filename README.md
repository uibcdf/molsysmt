MolSysMT
==============================

[![GitHub Actions Build Status](https://github.com/uibcdf/molsysmt/workflows/CI/badge.svg)](https://github.com/uibcdf/molsysmt/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/uibcdf/molsysmt/branch/master/graph/badge.svg)](https://codecov.io/gh/uibcdf/molsysmt/branch/master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue.svg)](https://www.python.org/downloads/) 
[![Install with conda](https://img.shields.io/badge/Install%20with-conda-brightgreen.svg)](https://conda.anaconda.org/uibcdf/molsysmt)
[![DOI](https://zenodo.org/badge/137937243.svg)](https://zenodo.org/badge/latestdoi/137937243)

**[Installation](#installation)** |
**[Documentation](#documentation)** |
**[License](#license)** |
**[Credits](#credits)** |
**[Team](#team)**


Molecular Systems Multi-Tool

This library was thought as a humble frontend to make the life of a computational molecular biology lab, the UIBCDF,  easier. 
MolSysMT is design to cover specific needs, or to speed up workflows, when you are working with tools such as:

- MDTraj
- MDAnalysis
- PDBFix
- OpenMM
- Yank
- HTMD
- PyEmma
- ParmEd
- NGLview
- pdbtools?

Although MolSysMT was not concived to do what other tools do better, this
toolkit can be used alone to do few simple tasks.

All credit should be given to the developers and mantainers of these former packages and the libraries they depend on.


Molecular Systems:
- Aqui deberia de ir todo el tema de la creacion del sistema molecular junto con parametros y topologia
- Deberia tambien estar esto preparado para trabajar con moleculas como ligandos.

poner ParmEd y OpenBabel:
parmed.github.io
http://openbabel.org/wiki/Main_Page

pdbfixer

Molecular Dynamics:

## Installation

### Dependencies

-Fortran Compiler (gfortran or intel fortran compiler)
-Lapack ('conda install lapack' would work?)

Other python packages as those mentioned here(link to section) and included in this list(file).


### Conda

#### Updating

### GitHub
```bash
git clone git@github.com:UIBCDF/MolSysMT.git
cd MolSysMT
python setup.py develop
```

```bash
pip uninstall molsysmt
```

#### Updating
To be written

## Documentation

http://www.uibcdf.org/MolSysMT/

## License

## Credits

All credit should be given to the developers and mantainers of the following tools and dependencies:

...

## Team

### Responsables

Diego Prada Gracia    
Liliana M. Moreno Vargas

### Contributors

...

## Citation

### Last version DOI:   
Cite the last version with the following DOI provided by Zenodo:    
<br/>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2530946.svg)](https://doi.org/10.5281/zenodo.2530946)    

### Cite all versions?
You can cite all versions by using the following DOI.
[This DOI represents all versions, and will always resolve to the latest one](http://help.zenodo.org/#versioning):    
<br/>
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2530945.svg)](https://doi.org/10.5281/zenodo.2530945)    
    

## Acknowledgments and Copyright

### Copyright

Copyright (c) 2021, UIBCDF


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.

