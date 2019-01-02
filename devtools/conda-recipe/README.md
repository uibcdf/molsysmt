# Instructions

## Conda packages required

```bash
conda install anaconda-client conda-build
```

## Building and pushing to https://anaconda.org/uibcdf

```bash
conda config --set anaconda_upload no
conda build .
conda build . --output # If needed
anaconda login
anaconda upload --user uibcdf /path/to/conda-package.tar.bz2
conda build purge
anaconda logout
```

## Additional Info
https://docs.anaconda.com/anaconda-cloud/user-guide/tasks/work-with-packages
