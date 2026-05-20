# MolSysMT Core Algorithms

This document specifies the internal algorithms that power the interoperability and performance of the MolSysMT framework.

---

## 1. Topological Normalization Specification

### 1.1 Overview
MolSysMT implements a **Normalization Engine** to resolve nomenclatural inconsistencies across force fields (AMBER, CHARMM, GROMOS) and data sources (PDB, MMTF).

### 1.2 Atom Name Pacification
- **Inference:** When a system is loaded, MolSysMT infers the chemical element (atom type) from the atom name.
- **Single Source of Truth:** `molsysmt/element/atom/names.py` contains ~250 mappings (e.g., `HN1` $\rightarrow$ `H`, `OW` $\rightarrow$ `O`).
- **Rule:** If a name is unrecognized, it produces `UNK` and a warning.

### 1.3 Residue (Group) Normalization
- **Mapping:** `molsysmt/element/group/amino_acid/group_types.py` (~817 entries).
- **Behavior:** Normalizes protonation states (`HIE` $\rightarrow$ `HIS`) and terminal variants.

---

## 2. Precision Policy Specification

### 2.1 Supported Precisions
1. **Single Precision (`float32`):** Used for disk I/O (XTC/DCD).
2. **Double Precision (`float64`):** The native standard for `molsysmt.MolSys` and internal performance kernels (`molsysmt.lib`).

### 2.2 Boundary Hardening
- **Public-to-Kernel:** Public wrappers (e.g., `get_rmsd()`) MUST cast input arrays to `np.float64` before calling JIT kernels.
- **In-memory Promotion:** When converting to `MolSys`, coordinates are promoted to `float64` to avoid redundant casting in subsequent analysis.

---

## 4. Group Type Inference Algorithm
MolSysMT classifies groups based on their atomic composition and name:
- **`water`:** Any group with a name in the canonical `_WATER_NAMES` set (`HOH`, `SOL`, `WAT`, etc.).
- **`ion`:** Any single-atom group representing a standard cation or anion.
- **`amino acid`:** Any group containing the minimal backbone quartet: `N`, `CA`, `C`, and `O`.
- **`small molecule`:** Any group not fitting the above criteria but having a consistent covalent block.
