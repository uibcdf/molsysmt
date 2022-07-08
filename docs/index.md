# MolSysMT

```{image} https://zenodo.org/badge/137937243.svg
:target: https://zenodo.org/badge/latestdoi/137937243
```

```{image} https://anaconda.org/uibcdf/molsysmt/badges/license.svg
:target: https://github.com/uibcdf/MolSysMT/blob/master/License
```

MolSysMT makes the work with molecular models and simulations easy.

## Install it

```bash
conda install -c uibcdf molsysmt
```
## Use it

```python
import molsysmt as msm

molsys = msm.convert('1BRS', selection='molecule_type=="protein"')

msm.info(molsys, element='molecule')

msm.structure.in_contact(molsysmt, element='molecule', threshold='2 angstroms')
msm.structure.neighbors_lists(molsysmt, element='molecule', threshold='2 angstroms')

barnase = msm.extract(molsys, selection="chain_name=='B'")
barstar_E = msm.extract(molsys, selection="chain_name=='E")
barstar_F = msm.extract(molsys, selection="chain_name=='F'")

barstar = msm.structure.align(barstar_F, selection='atom_name=="CA"',
                              reference_molecular_system=barstar_E, reference_selection='atom_name=="CA"',
                              engine_1='MolSysMT', engine_2='biopython')

molsys = msm.merge([barnase, barstar])

msm.build.get_missing_heavy_atoms(molsys, engine=)

msm.info(molsys, element='entity')

msm.cite()
```


```{eval-rst}
.. toctree::
   :name: about
   :caption: About
   :maxdepth: 2
   :hidden:

   contents/about/what.md
   contents/about/installation.md
   contents/about/showcase/index.md
   contents/about/citation.md

.. toctree::
   :name: user_guide
   :caption: User Guide
   :maxdepth: 2
   :hidden:

   contents/user/intro/index.md
   contents/user/tools/index.md
   contents/user/native_forms/index.md

.. toctree::
   :name: developer_guide
   :caption: Developer Guide
   :maxdepth: 2
   :hidden:

   contents/developer/intro/index.md
   contents/developer/new_form.ipynb
   contents/developer/documentation/index.md

.. toctree::
   :name: api_doc
   :caption: API Documentation
   :maxdepth: 1
   :hidden:

   api_tools.md
   api_forms.md
   api_thirds.md
```
