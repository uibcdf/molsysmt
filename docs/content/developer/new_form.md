# Implementing a New Form Adapter

This guide explains how to add support for a new molecular system format, class, or representation (referred to as a **"form"**) in MolSysMT. 

By implementing a form adapter, your representation automatically gains the ability to:
1.  Participate in the polymorphic **conversion graph** (`molsysmt.convert`).
2.  Expose properties natively via the **dispatch engine** (`molsysmt.get`).
3.  Support memory-safe chunked execution on heavy trajectories using **structure iterators**.

---

## 1. Directory Structure and Naming Conventions

All form adapters are located under `molsysmt/form/`. The directory name and the internal `form_name` variable follow a strict pattern based on the **form type**:

| Form Type | Target Representation | Directory Name | Canonical `form_name` |
| :--- | :--- | :--- | :--- |
| **`class`** | In-memory library objects | `<library>_<Class>` (e.g. `rdkit_Mol`) | `<library>.<Class>` (e.g. `'rdkit.Mol'`) |
| **`file`** | Physical file formats on disk | `file_<format>` (e.g. `file_pdb`) | `file:<format>` (e.g. `'file:pdb'`) |
| **`string`** | Text inputs and identifiers | `string_<format>` (e.g. `string_smiles`) | `string:<format>` (e.g. `'string:smiles'`) |

---

## 2. Step 1: Scaffolding a New Form Adapter

To ensure your new form adapter conforms perfectly to the repository's QA contract, use the developer template scaffolding tool:

```bash
python devtools/scripts/scaffold_form.py --name <form_folder_name> --type <class/file/string> [--class-name <class_name>]
```

### Example (Class Form):
```bash
python devtools/scripts/scaffold_form.py --name openff_Topology --type class --class-name "openff.toolkit.topology.Topology"
```

### Example (File Form):
```bash
python devtools/scripts/scaffold_form.py --name file_xyz --type file
```

This command automatically templates a pristine adapter folder containing:
*   `__init__.py` (Core contract metadata)
*   `is_form.py` (Form detection callable)
*   `attributes.py` (Supported attribute map)
*   `has_attribute.py` (Attribute check callable)
*   `iterators.py` (Boilerplate for structure and topology iterators)
*   `get_topological_attributes.py` (Topological property getters)
*   get_structural_attributes.py (Structural property getters)

---

## 3. Step 2: Implementing the Core Contract

### A. Form Detection (`is_form.py`)
Implement the detection logic in `is_form(item)`. This must return `True` only if the incoming object matches the expected signature of this form.

```python
def is_form(item):
    """Check if the item is of form 'rdkit.Mol'."""
    output = False
    class_name = str(type(item))
    if 'rdkit.Chem.rdchem.Mol' in class_name:
        output = True
    return output
```

### B. Attributes and Getters (`attributes.py` & `has_attribute.py`)
The `attributes` dictionary in `attributes.py` maps supported attributes to `True` or `False`. 
*   **Rule**: An attribute must be marked `True` if and only if a corresponding getter function (e.g. `get_n_atoms` or `get_coordinates`) is fully implemented in `get_topological_attributes.py` or `get_structural_attributes.py`.

In `has_attribute.py`, define the check decorated with the argument digest validation:

```python
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='rdkit.Mol')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    from .attributes import attributes
    return attributes.get(attribute, False)
```

---

## 4. Step 3: Lazy Imports & Dependency Isolation

> [!CAUTION]
> **Never Import Soft Dependencies Eagerly**
> MolSysMT maintains an extremely fast cold import latency. Eager imports of libraries like `openmm`, `mdtraj`, `rdkit`, or `biopython` at the module level in `__init__.py` or any adapter file will leak and break the package.
> **All soft dependencies must be imported lazily inside functions.**

For example:
```python
# INCORRECT:
import rdkit # Eager import at top level will fail the QA audit

# CORRECT:
def get_n_atoms(item, skip_digestion=False):
    from rdkit import Chem # Lazy import inside the function body
    return item.GetNumAtoms()
```

---

## 5. Step 4: Implementing Iterators (Heavy Forms)

If your form represents a trajectory or a heavy coordinate file, you must implement iterators to support block-wise execution:
1.  Open `iterators.py`.
2.  Subclass `BaseStructuresIterator` or `BaseTopologyIterator` from `molsysmt/form/iterators.py`.
3.  Implement `__init__`, `__next__`, and `close()`. Context manager protocols (`__enter__` and `__exit__`) are inherited automatically.

```python
from molsysmt.form.iterators import BaseStructuresIterator

class StructuresIterator(BaseStructuresIterator):
    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1,
                 structure_indices=None, skip_digestion=True):
        self.molecular_system = molecular_system
        # Open coordinate file handles

    def __next__(self):
        # Yield coordinates chunk, or raise StopIteration when done
        pass

    def close(self):
        # Safely release file locks or handles
        pass
```

---

## 6. Step 5: Implementing Conversions

1.  Write a converter module under your folder named `to_<target_form>.py`.
2.  Import and use `@arg_digest` with the source form name.
3.  Implement the conversion, returning the target form object.
4.  Register it in the `_convert_to` dictionary in `__init__.py` using the **string name** of the function to maintain lazy loading:

```python
# molsysmt/form/my_form/__init__.py
_convert_to = {
    'molsysmt.MolSys': 'to_molsysmt_MolSys',
    'molsysmt.Topology': 'to_molsysmt_Topology',
}
```

---

## 7. Step 6: Verifying with the QA Conformance Linter

Before submitting any Pull Request, run the automated linter to verify your new form adapter:

```bash
python devtools/scripts/validate_form_adapters.py
```

The linter automatically scans all folders in `molsysmt/form/` and audits them against the developer contract. If any issues are found (e.g. missing metadata, eager imports, non-conforming iterators), it will output detailed error logs and exit with code `1`.
