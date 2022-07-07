
.. molsysmt documentation master file

========
MolSysMT
========

.. image:: https://zenodo.org/badge/137937243.svg
   :target: https://zenodo.org/badge/latestdoi/137937243

.. image:: https://anaconda.org/uibcdf/molsysmt/badges/license.svg
   :target: https://github.com/uibcdf/MolSysMT/blob/master/License

MolSysMT, Molecular System Multi-Tool, is a swiss army knife to make the researchers life easier and the learning barrier of new lab student lower. This is done by simplifying the sintaxis of your script and reducing the amount of commands you have to remind to have some simple stuff done. Just that. In this sense MolSysMT is probably better defined as a 'front-end', a 'wrapper' o meta-library. Thereby all credit should be given to the fellows who developed and push those tools in the core of MolSysMT as openmm, mdtraj, yank, mdanalysis, parmed, nglview, and many others gratefully listed in the main README.md file of the source repository.

Exceptionally few home-made subroutines will be included here to fill specific gaps in our needs. But this should not be, in principle, the main purpose of MolSysMT.

.. warning:: |IntroWarningText|

.. |IntroWarningText| replace::
        At this moment MolSysMT is a work in progress project maintened by the UIBCDF Lab. It was concieved as a central repository for those shortcuts and common routines in the daily workflow of our lab. If you think this library is useful to you, use it with caution. Any feedback is welcome.

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
   contents/developer/documentation/index.rst

.. toctree::
   :name: api_doc
   :caption: API Documentation
   :maxdepth: 1
   :hidden:

   api_tools.rst
   api_items.rst
   api_thirds.rst

