.. _API Native Queries:

Native query methods
====================

These resident-object methods share the basic query vocabulary and outputs.
Use keyword arguments when switching from free functions: existing native
positional syntax is preserved. Molecular metadata queries on Interactions
complement its specialized sparse occurrence queries.

.. automethod:: molsysmt.native.MolSys.get

.. automethod:: molsysmt.native.MolSys.info

.. automethod:: molsysmt.native.Topology.get

.. automethod:: molsysmt.native.Topology.info

.. automethod:: molsysmt.native.Structures.get

.. automethod:: molsysmt.native.Structures.info

.. automethod:: molsysmt.native.ChemicalStates.get

.. automethod:: molsysmt.native.ChemicalStates.info

.. automethod:: molsysmt.native.MolSysBuilder.get

.. automethod:: molsysmt.native.MolSysBuilder.info

.. automethod:: molsysmt.Interactions.get

.. automethod:: molsysmt.Interactions.info

.. _API Native Structure Inputs:

Constructing and appending Structures
-------------------------------------

Native structure inputs retain explicit physical units and a shared structure
axis. Temperature and energies accept a real scalar for one structure or a
one-dimensional series. Query output follows the active unit policy.

.. automethod:: molsysmt.native.Structures.__init__

.. automethod:: molsysmt.native.Structures.append

.. _API Native Group Membership:

Declaring group membership
--------------------------

Partial topologies can declare ordered chain/group membership without an atom
inventory. Existing atom-level evidence must agree with the declaration.

.. autoproperty:: molsysmt.native.Topology.chain_groups

.. automethod:: molsysmt.native.Topology.set_chain_groups
