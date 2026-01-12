# Fork MolSysMT

## Clone your fork

The raw code fully alive can be cloned from the [github repository](https://github.com/uibcdf/MolSysMT) as follows:

```bash
git clone https://github.com/uibcdf/MolSysMT.git
```

or with the native GitHub cli:

```bash
gh repo clone uibcdf/MolSysMT
```

If you are going to contribute to the code, having a look to the Developer Guide is strongly suggested. 

## Work with a conda environment

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

## Install it

Having the dependencies solved, the command to install MolSysMT from its source code is:

```bash
cd MolSysMT
python setup.py develop
```

