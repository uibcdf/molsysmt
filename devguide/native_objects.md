# Native Objects

This document defines the invariants, responsibilities, and expected behavior for the core native objects of MolSysMT. These objects constitute the **Tier 1** foundation of the framework.

---

## 1. The Core Trinity

MolSysMT architecture is built around three primary native classes:

### `molsysmt.native.MolSys`
The high-level orchestrator. It is a container that synchronizes a `Topology` object and a `Structures` object. 
- **Responsibility:** Ensure that any operation (like `extract` or `merge`) is applied atomically to both topology and structures, maintaining index consistency.
- **Invariants:** The number of atoms in the `Topology` must always match the second dimension (atoms) of the coordinates in `Structures`.

### `molsysmt.native.Topology`
The manager of structural identities and connectivity.
- **Responsibility:** Store and query the covalent graph and hierarchical metadatos (names, IDs, types).
- **Invariants:** All element IDs (`atom_id`, `group_id`, etc.) are stored as **strings** to ensure compatibility across different file formats.

### `molsysmt.native.Structures` (formerly Trajectory)
The manager of physical, time-dependent data.
- **Responsibility:** Handle coordinates, velocities, boxes, and time steps.
- **Centralized Logic (1.0.0 Refactor):** Since the 1.0.0 stability pass, `Structures` centralizes all low-level property access through dedicated methods (`get_coordinates`, `set_coordinates`, `get_box`, etc.). This avoids logic duplication in form adapters.
- **Invariants:** 
    - Coordinates and boxes follow the shapes and units defined in `data_model.md`.
    - Physical properties are always returned as **Quantities** via `pyunitwizard`.

---

## 2. Invariants & Behaviors

### Element IDs
- All IDs must be **strings**. If a source (like a list of integers) provides numeric IDs, they must be normalized upon object creation or conversion.

### Handling Missing Data
- If a structural attribute (e.g., `velocities`) is missing, the `get` method should return a list of `None` with a length equal to the number of structures, or an empty Quantity array if appropriate, but never raise a bare `AttributeError`.

### Native Method Decorators
- Methods in native objects that interact with MolSysMT arguments (like selections or indices) must be decorated with `@arg_digest()` to maintain consistency with the public API.

---

## 3. Operations

### Extraction & Merging
- Native objects must implement their own `extract()` and `add()` methods. 
- These methods are responsible for reindexing the system correctly (e.g., ensuring atom indices start from 0 after an extraction).

### SMonitor Integration
- All native methods must emit signals through **SMonitor** to allow traceability of errors during complex pipelines.
