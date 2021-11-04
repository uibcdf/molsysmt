
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
   :name: intro
   :caption: Installation and Quick Guide
   :maxdepth: 1

   contents/intro/Installation.md
   contents/intro/Quickstart.ipynb

.. toctree::
   :name: molsys
   :caption: Molecular Systems
   :maxdepth: 1

   contents/molsys/Molecular_Systems_Items_Forms.ipynb
   contents/molsys/Elements.md
   contents/molsys/MolSys.md
   contents/molsys/native/index.rst

.. toctree::
   :name: basic
   :caption: Basic
   :maxdepth: 1

   contents/basic/get_form.ipynb
   contents/basic/info.ipynb
   contents/basic/selection.ipynb
   contents/basic/get.ipynb
   contents/basic/set.ipynb
   contents/basic/contains.ipynb
   contents/basic/is_composed_of.ipynb
   contents/basic/compare.ipynb
   contents/basic/convert.ipynb
   contents/basic/extract.ipynb
   contents/basic/copy.ipynb
   contents/basic/merge.ipynb
   contents/basic/remove.ipynb
   contents/basic/add.ipynb
   contents/basic/append_frames.ipynb
   contents/basic/concatenate_frames.ipynb
   contents/basic/view.ipynb

.. toctree::
   :name: building
   :caption: Building
   :maxdepth: 1

   contents/build/has_hydrogens.ipynb
   contents/build/add_hydrogens.ipynb
   contents/build/remove_hydrogens.ipynb
   contents/build/get_missing_heavy_atoms.ipynb
   contents/build/add_missing_heavy_atoms.ipynb
   contents/build/get_missing_residues.ipynb
   contents/build/get_missing_terminals.ipynb
   contents/build/get_non_standard_residues.ipynb
   contents/build/add_terminal_cappings.ipynb
   contents/build/is_solvated.ipynb
   contents/build/solvate.ipynb
   contents/build/remove_solvent.ipynb
   contents/build/build_peptide.ipynb
   contents/build/model_loop.ipynb
   contents/build/mutate.ipynb

.. toctree::
   :name: topology
   :caption: Topology
   :maxdepth: 1

   contents/topology/get_bondgraph.ipynb
   contents/topology/get_covalent_blocks.ipynb
   contents/topology/get_covalent_chains.ipynb
   contents/topology/get_covalent_dihedral_quartets.ipynb
   contents/topology/get_covalent_sequence_alignment.ipynb
   contents/topology/get_covalent_sequence_identity.ipynb

.. toctree::
   :name: structure
   :caption: Structure
   :maxdepth: 1
   contents/structure/get_center.ipynb
   contents/structure/get_contacts.ipynb
   contents/structure/get_dihedral_angles.ipynb
   contents/structure/get_distances.ipynb
   contents/structure/get_least_rmsd.ipynb
   contents/structure/get_min_max_distances.ipynb
   contents/structure/get_neighbors.ipynb
   contents/structure/get_radius_of_gyration.ipynb
   contents/structure/get_ramachandran_angles.ipynb
   contents/structure/get_rmsd.ipynb
   contents/structure/get_sasa.ipynb
   contents/structure/translate.ipynb
   contents/structure/center.ipynb
   contents/structure/set_dihedral_angles.ipynb
   contents/structure/shift_dihedral_angles.ipynb
   contents/structure/align.ipynb
   contents/structure/fit.ipynb

.. toctree::
   :name: pbc
   :caption: Periodic Boundary Conditions
   :maxdepth: 1

   contents/pbc/box_angles_from_box_vectors.ipynb
   contents/pbc/box_lengths_from_box_vectors.ipynb
   contents/pbc/box_shape_from_box_angles.ipynb
   contents/pbc/box_shape_from_box_vectors.ipynb
   contents/pbc/box_vectors_from_box_lengths_and_angles.ipynb
   contents/pbc/box_volume_from_box_vectors.ipynb
   contents/pbc/wrap_to_pbc.ipynb
   contents/pbc/wrap_to_mic.ipynb
   contents/pbc/unwrap.ipynb

.. toctree::
   :name: hbonds
   :caption: Hydrogen bonds
   :maxdepth: 1

   contents/hbonds/hbonds.ipynb

.. toctree::
   :name: physchem
   :caption: Physico-chemical Properties
   :maxdepth: 1

   contents/physchem/area_buried.ipynb
   contents/physchem/atomic_radius.ipynb
   contents/physchem/buried_fraction.ipynb
   contents/physchem/charge.ipynb
   contents/physchem/hydrophobicity.ipynb
   contents/physchem/mass.ipynb
   contents/physchem/polarity.ipynb
   contents/physchem/surface_area.ipynb
   contents/physchem/transmembrane_tendency.ipynb
   contents/physchem/volume.ipynb

.. toctree::
   :name: molmech
   :caption: Molecular Mechanics
   :maxdepth: 1

   contents/molmech/force_fields.ipynb
   contents/molmech/energy_minimization.ipynb
   contents/molmech/molecular_mechanics.ipynb
 
.. toctree::
   :name: working_with
   :caption: Working With
   :maxdepth: 1

   contents/working_with/openmm.ipynb
   contents/working_with/nglview.ipynb

.. toctree::
   :name: help
   :caption: Help
   :maxdepth: 1

   contents/help/help.ipynb

.. toctree::
   :name: demo
   :caption: Demo Systems
   :maxdepth: 1

   contents/demo/demo.ipynb
   contents/demo/barnase_barstar-Copy1.ipynb
   contents/demo/barnase_barstar.ipynb
   contents/demo/DHFR.ipynb
   contents/demo/T4_Lysozyme_L99A.ipynb
   contents/demo/two_LJ_particles.ipynb
   contents/demo/villin_hp35.ipynb
   contents/demo/villin_hp35_2.ipynb

.. toctree::
   :caption: API Documentation
   :maxdepth: 1

   api/index.rst
   api/index_elements

Glossary, indices and tables
============================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

