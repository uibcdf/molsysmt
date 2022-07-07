
.. molsysmt documentation master file

========
MolSysMT
========

.. image:: https://zenodo.org/badge/137937243.svg
   :target: https://zenodo.org/badge/latestdoi/137937243

.. image:: https://anaconda.org/uibcdf/molsysmt/badges/license.svg
   :target: https://github.com/uibcdf/MolSysMT/blob/master/License

MolSysMT makes the work with molecular models and simulations easy.

Install it.

```bash
conda install -c uibcdf molsysmt
```

Import it.

```python
import molsysmt as msm
```

Make use of the native objects, methods, and syntaxis, to ensemble your daily workflows.

```python
molsys = msm.convert('1BRS', selection='molecule_type=="protein"')

msm.info(molsys, element='chain')

barnase = msm.extract(molsys, selection="chain_name=='B'")
barstar_E = msm.extract(molsys, selection="chain_name=='E")
barstar_F = msm.extract(molsys, selection="chain_name=='F'")

msm.get_minimum_distance(barnase, barstar_E)

msm.get_minimum_distance(barnase, barstar_F)
```


Integrate your favorite third libraries.

```python
id, bla, bla = msm.structure
barstar = msm.structure.align(barstar_F, selection='atom_name=="CA"',
                              reference_molecular_system=barstar_E, reference_selection='atom_name=="CA"',
                              engine_1='MolSysMT', engine_2='biopython')

molsys = msm.merge([barnase, barstar])

msm.build.get_missing_heavy_atoms(molsys, engine=)

msm.info(molsys, element='entity')

```

Report your results citing the used tools.

```python
msm.cite()

```

.. toctree::
   :name: about
   :caption: About
   :maxdepth: 2
   :hidden:

   contents/about/what.md
   contents/about/installation.md
   contents/about/showcase/index.rst

.. toctree::
   :name: user_guide
   :caption: User Guide
   :maxdepth: 2
   :hidden:

   contents/user/intro/index.rst
   contents/user/tools/index.rst
   contents/user/native_forms/index.rst

.. toctree::
   :name: developer_guide
   :caption: Developer Guide
   :maxdepth: 2
   :hidden:

   contents/developer/intro/index.rst
   contents/developer/new_form.ipynb
   contents/developer/documentation/index.rst

.. toctree::
   :name: api_doc
   :caption: API Documentation
   :maxdepth: 1
   :hidden:

   api_tools.rst
   api_forms.rst
   api_thirds.rst

