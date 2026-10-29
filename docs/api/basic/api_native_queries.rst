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

Reading stored chemical axes
-----------------------------

ChemicalStates.get reads shared atom positions, state-local bond/component
positions, stored counts, membership, completeness, atom assignments, bond fields
and component labels without constructing Topology. Formal charges retain integer
multiples of the elementary charge. Unknown atom columns return None; missing
bond fields retain nullable entries per selected edge. Stereo references retain
two independently nullable atom indices per edge. State inventory remains
collection-wide. A zero-state collection
retains its atom domain but cannot supply chemical counts. See
:ref:`user-foundations-native-world-classes-molsysmt-chemicalstates` for the
implemented element/attribute table and experimental migration boundary.

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

.. _API Native Molecule Membership:

Declaring atom molecule membership
----------------------------------

Ungrouped atom ownership is independent of chemical components. Grouped atoms
inherit their group's owner; declarations must agree with that hierarchy.

.. automethod:: molsysmt.native.Topology.set_atom_molecules

.. _API Native Chemical Editing:

Editing selected chemical states
----------------------------------------

These native operations stage selected-state graph/component data before
publication. They preserve other states and stable inventory and do not run
chemical perception or interaction detectors.

.. automethod:: molsysmt.native.ChemicalStates.get_bonds

.. automethod:: molsysmt.native.ChemicalStates.add_bonds

.. automethod:: molsysmt.native.ChemicalStates.remove_bonds

.. automethod:: molsysmt.native.ChemicalStates.rebuild_components
