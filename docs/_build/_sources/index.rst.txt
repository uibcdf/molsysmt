
.. molmodmt documentation master file

========
MolModMT
========

.. image:: https://zenodo.org/badge/137937243.svg
   :target: https://zenodo.org/badge/latestdoi/137937243

.. image:: https://anaconda.org/uibcdf/molmodmt/badges/license.svg
   :target: https://github.com/uibcdf/MolModMT/blob/master/License

MolModMT, Molecular Models Multi-Tool, is a swiss army knife to make the researchers life easier and the learning barrier of new lab student lower. This is done by simplifying the sintaxis of your script and reducing the amount of commands you have to remind to have some simple stuff done. Just that. In this sense MolModMT is probably better defined as a 'front-end', a 'wrapper' o meta-library. Thereby all credit should be given to the fellows who developed and push those tools in the core of MolModMT as openmm, mdtraj, yank, mdanalysis, parmed, nglview, and many others gratefully listed in the main README.md file of the source repository.

Exceptionally few home-made subroutines will be included here to fill specific gaps in our needs. But this should not be, in principle, the main purpose of MolModMT.

.. warning:: |IntroWarningText|

.. |IntroWarningText| replace::
        At this moment MolModMT is a work in progress project maintened by the UIBCDF Lab. It was concieved as a central repository for those shortcuts and common routines in the daily workflow of our lab. If you think this library is useful to you, use it with caution. Any feedback is welcome.

.. note:: |IntroNoteText|

.. |IntroNoteText| replace::
        A version of this web page in spanish will be available soon.

.. toctree::
   :caption: Installation and Quick Guide
   :maxdepth: 1

   Installation.md
   Quickstart.ipynb

.. toctree::
   :caption: User Guide
   :maxdepth: 2

   Forms.ipynb
   Selection.ipynb
   MolMod.md
      Elements.md

.. toctree::
   :caption: API Documentation
   :maxdepth: 1

   api/index
   api/index_elements

Glossary, indices and tables
============================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

