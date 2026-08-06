(user-foundations-native-world-molsysbuilder)=
# molsysmt.MolSysBuilder

`molsysmt.MolSysBuilder` is an editable native class designed for step-by-step assembly, incremental construction, and modification of molecular systems in MolSysMT.

---

## Role and Purpose

Unlike `molsysmt.MolSys`—which represents a materialized, immutable molecular system—`molsysmt.MolSysBuilder` acts as a dynamic staging container. It enables users and internal constructors to build molecular topologies from scratch by declaring atoms, groups, chains, molecules, entities, and bonds incrementally, as well as assigning structural coordinates before final system materialization.

---

## Internal Architecture

The `molsysmt.MolSysBuilder` class manages staging components for system assembly:

- **Topological Assembly**: Provides methods to declare individual atoms (`add_atom`), residue groups (`add_group`), components (`add_component`), chains (`add_chain`), molecules (`add_molecule`), entities (`add_entity`), and covalent bonds (`add_bond`).
- **Structural Assignment**: Accepts coordinate arrays (`set_coordinates`) and periodic boundary box vectors.
- **System Materialization**: The `.build()` method validates accumulated topological and structural contracts and materializes a unified, canonical `molsysmt.MolSys` instance.

---

## Design Invariants

The `molsysmt.MolSysBuilder` class enforces specific operational principles:

- **Canonical Index Alignment**: Atom additions and group associations are tracked in increasing source-index order to guarantee that topology and coordinate arrays remain strictly synchronized.
- **Pre-materialization Introspection**: Declared chemical and topological attributes can be inspected before final materialization.
- **Scope Boundaries**: Focuses on topological graph assembly and structural coordinate staging; force-field mechanics and explicit per-structure chemical state associations are handled after materialization.
