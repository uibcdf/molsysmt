
.. currentmodule:: molmodmt

#################
API Documentation
#################

Basic manipulations
-------------------

General and basic methods to operate with molecular models and their forms.

.. autosummary::
   :toctree: _autosummary

   load
   get_form
   get
   set
   info
   select
   convert
   extract
   merge
   write
   view

Transformations
---------------

Methods to change any property of a molecular model, structural or topological, without changing its
form.

.. autosummary::
   :toctree: _autosummary

   set
   remove
   remove_solvent
   add_missing_hydrogens
   recenter
   fix_chains
   fix_pdb_structure
   add_loop

Observables
-----------

Methods to extract structural or topological observables of a molecular model.

.. autosummary::
   :toctree: _autosummary

   get
   distances
   contact_map
   neighbors_lists
   center_of_mass
   geometrical_center
   radius_of_gyration

Comparisons
------------------------------------

Methods to extract structural or topological observables of a molecular model.

.. autosummary::
   :toctree: _autosummary

   rmsd
   least_rmsd_fit
   sequence_identity
   sequence_alignment
   structure_alignment

Modeling
--------

.. autosummary::
   :toctree: _autosummary

   add_loop


Glossary
--------

* :ref:`genindex`
* :ref:`search`
