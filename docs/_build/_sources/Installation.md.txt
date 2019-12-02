# Installation

The latest "stable" version of MolModMT can be installed from the UIBCDF Anaconda channel:

```bash
conda -c uibcdf molmodmt
```

If you want to work with the not so tested last beta version, the installation command is the following:

```bash
conda install -c uibcdf/label/dev molmodmt
```

The former beta version is nothing but a quenched version from the main github repository of this project which it is done from time to time with few scruples. The raw code fully alive can be installed from this github repo as follows:

```bash
git clone https://github.com/uibcdf/MolModMT.git
cd MolModMT
python setup.py develop
```

In the first two cases, MolModMT can be uninstalled with conda:

```bash
conda remove molmodmt
```

But if you installed MolModMT straight from its github central repository, do the following to uninstall it:

```bash
pip uninstall molmodmt
```
