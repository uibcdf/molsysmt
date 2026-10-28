API Bond
========

.. currentmodule:: molsysmt.element.bond

These data support covalent-bond candidate heuristics. They are not a general
valence model, bond-order assignment or certificate of chemically complete
connectivity. The stored lengths carry physical units; use PyUnitWizard to
convert them explicitly when comparing with coordinates.

.. py:data:: max_expected_bond_length

   Nested mapping of group categories and element-type pairs to length
   quantities, with ``None`` for an explicitly unavailable pair. The stored
   values use angstroms. Only the listed categories and pairs are covered.

.. py:data:: bond_length_tolerance

   Additional length tolerance used with the expected bond-length table.
   This is a unit-bearing quantity stored in angstroms.
