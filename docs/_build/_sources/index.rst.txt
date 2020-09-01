
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

.. note:: |IntroNoteText|

.. |IntroNoteText| replace::
        A version of this web page in spanish will be available soon.

.. toctree::
   :name: installation_quickguide
   :caption: Installation and Quick Guide
   :maxdepth: 1

   contents/Installation.md
   contents/Quickstart.ipynb

.. toctree::
   :name: forms_elements
   :caption: Forms and elements
   :maxdepth: 1

   contents/Forms.ipynb
   contents/Elements.md
   contents/MolSys.md

.. toctree::
   :name: basic_manipulations
   :caption: Basic tools
   :maxdepth: 1

   contents/Convert.ipynb
   contents/Selection.ipynb
   contents/Get.ipynb
   contents/Info.ipynb
   contents/Copy.ipynb
   contents/Extract.ipynb
   contents/Remove.ipynb
   contents/View.ipynb

.. toctree::
   :name: building_system
   :caption: Building tools
   :maxdepth: 1

   contents/Fix.ipynb
   contents/Solvation.ipynb
   contents/Protonation.ipynb
   contents/Build_peptide.ipynb
   contents/Terminal_capping.ipynb
   contents/Model_loop.ipynb
   contents/Energy_minimization.ipynb
   contents/Constraints_and_restraints.ipynb

.. toctree::
   :name: structural_observables
   :caption: Structural tools
   :maxdepth: 1

   contents/Distances.ipynb
   contents/PBC.ipynb
   contents/Centers.ipynb
   contents/RMSD.ipynb
   contents/Rg.ipynb
   contents/Dihedral_angles.ipynb
   contents/SASA.ipynb

.. toctree::
   :name: topological_observables
   :caption: Topological tools
   :maxdepth: 1

   contents/Bondgraph.ipynb
   contents/Covalent_chains.ipynb
   contents/Alignment.ipynb
   contents/Mutations.ipynb

.. toctree::
   :name: physchem_admet_observables
   :caption: PhysChem and ADMET tools
   :maxdepth: 1

   contents/Mass.ipynb
   contents/Volume_and_radii.ipynb
   contents/Charge.ipynb
   contents/Polarity.ipynb
   contests/Transmembrane_tendency.ipynb

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

