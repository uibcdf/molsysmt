# MolSysMT Interface Specification

## 1. Selection Language & Syntax
Selections are the primary way users address subsets of a molecular system.

### 1.1 Grammar Principles
- **0-based indexing:** All numeric indices start from 0.
- **Form-agnostic:** The same selection string (e.g., `'chain_name == "A"'`) must work across all forms (PDB, native, etc.) due to Topological Normalization.
- **Syntaxes:** The default is `MolSysMT`. Other syntaxes (like `MDTraj` or `Amber`) may be supported depending on the backend.

### 1.2 Syntax Responsibilities
- Parsing logic lives in `molsysmt/_private/selection/`.
- If a requested syntax is not supported for a specific form, a `NotSupportedSyntaxError` must be raised.

---

## 2. I/O and File Registry
MolSysMT treats files as just another Form of a molecular system.

### 2.1 File Handlers
- Every supported file format has a corresponding handler in `molsysmt/form/`.
- **Lazy Loading Policy:** Only **Binary Formats** (e.g., `H5MSM`, `XTC`, `DCD`) support true lazy loading of coordinates. **Text Formats** (e.g., `PDB`, `GRO`) generally perform **Eager Loading** of structural data during the initial topology parsing due to format constraints.

### 2.2 Remote PDB Retrieval
- When a `pdb_id` string is provided, MolSysMT attempts retrieval in a fixed priority order:
  1. `bcif.gz` (High-performance standard)
  2. `bcif`
  3. `cif.gz`
  4. `pdb` (Legacy standard)

---

## 3. Third-party Bridges
MolSysMT acts as a middleware between structural biology engines.

### 3.1 Diplomatic Policy
- MolSysMT does not replace MDAnalysis or OpenMM; it provides native adapters to "teleport" data into them.
- Bridges are maintained in `molsysmt/third_party/`.

### 3.2 Conversion Integrity
- Any conversion to a third-party object (e.g., `to_form='openmm.Modeller'`) must preserve the fundamental topology (atoms, bonds, residues) defined in the MolSysMT Trinity.
