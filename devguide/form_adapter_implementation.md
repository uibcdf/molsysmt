# Form Adapter Implementation & QA Conformance Guide

This document defines the official developer contract, scaffolding tools, and quality assurance workflows for implementing and maintaining molecular system form adapters in MolSysMT.

---

## 1. Core Architecture & Naming Conventions

MolSysMT is designed as a polymorphic conversion engine. To support diverse third-party structures, classes, and file formats, every supported representation (a **"form"**) is managed by a form adapter located under `molsysmt/form/<form_name_folder>/`.

### Directory and Form Names
Form adapters follow a strict mapping scheme based on their **form type**:
*   **`class`**: Represents in-memory library objects (e.g., `rdkit.Mol`, `biopython.Seq`). Folder names use underscores (e.g., `rdkit_Mol`), and `form_name` uses dots (`'rdkit.Mol'`).
*   **`file`**: Represents physical file formats on disk (e.g., `.pdb`, `.gro`). Folder names use `file_<format>` (e.g., `file_pdb`), and `form_name` uses colons (`'file:pdb'`).
*   **`string`**: Represents identifier/text sequence inputs (e.g., SMILES, UniProt IDs). Folder names use `string_<format>` (e.g., `string_pdb_id`), and `form_name` uses colons (`'string:pdb_id'`).

---

## 2. The Form Adapter Contract

Every adapter subdirectory must define a set of contract variables and callables.

### Required Module Variables (`__init__.py`)
*   `form_name` (str): The canonical name of the form (e.g. `'biopython.PDBStructure'`).
*   `form_type` (str): One of `'class'`, `'file'`, or `'string'`.
*   `form_info` (list): Metadata description list.
*   `bonds_are_explicit` (bool): True if chemical bonds are natively stored and accessible.
*   `bonds_can_be_computed` (bool): True if bonds can be computed from coordinates/geometry.
*   `piped_topological_attribute` (str or None): Name of a form to pipe topology queries to (e.g., `'molsysmt.Topology'`).
*   `piped_structural_attribute` (str or None): Name of a form to pipe structural queries to.
*   `piped_any_attribute` (str or None): Name of a form to pipe any fallback queries to.
*   `_convert_to` (dict): A lazy converter map where keys are target form names and values are **strings** of the converter function names (e.g., `{'molsysmt.Topology': 'to_molsysmt_Topology'}`).

### Required Callables
*   `is_form(item)` (callable): Checks if an incoming item matches the structural format or class signature of this form. Return `True` or `False`. Must live in `is_form.py`.
*   `has_attribute(item, attribute, include_none=False, skip_digestion=False)` (callable): Returns `True` if the form natively supports a given attribute. Must live in `has_attribute.py`.
*   `attributes` (dict/set/list): A static representation of supported attributes mapped to booleans. Must live in `attributes.py`.

---

## 3. Dependency Management & Import Isolation

> [!IMPORTANT]
> **No Eager Soft Dependencies at Top Level**
> Under no circumstances should soft dependencies (e.g., `openmm`, `mdtraj`, `rdkit`, `biopython`, `Bio`) be imported at the module level in `__init__.py` or any adapter file. This is to keep cold import times extremely fast. Always perform imports lazily inside functions.

### Argument Digestion Decorator
Public-facing adapter functions (like `has_attribute`, getters, and converters) must be decorated with `@arg_digest` to perform input validation:
```python
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='biopython.PDBStructure')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    from .attributes import attributes
    return attributes.get(attribute, False)
```
Private helper functions (under `molsysmt/_private`) must **not** use the digestion decorator.

---

## 4. Heavy Trajectories & Base Iterators

Heavy form adapters (e.g., trajectories, large coordinate files) must expose iterators to support block processing via the `ChunkedExecutor`.
Your form's `iterators.py` should subclass the developer base classes defined in `molsysmt/form/iterators.py`:

```python
from molsysmt.form.iterators import BaseStructuresIterator, BaseTopologyIterator
from molsysmt._private.smonitor import NotImplementedIteratorError

class StructuresIterator(BaseStructuresIterator):
    """
    Inherits __enter__, __exit__, and __iter__ from BaseStructuresIterator.
    Subclasses only need to implement __init__, __next__, and optionally close().
    """

    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1,
                 structure_indices=None, skip_digestion=True):
        self.molecular_system = molecular_system
        # Open handles / prepare files here

    def __next__(self):
        # Yield next coordinate chunk, or raise StopIteration
        raise NotImplementedIteratorError

    def close(self):
        # Release file locks/handles safely
        pass
```

---

## 5. Developer Scaffolding API

To easily create new form adapters that conform perfectly to the QA contract, use the template scaffolding utility `scaffold_form.py`:

```bash
python devtools/scripts/scaffold_form.py --name <form_name> --type <class/file/string> [--class-name <class_name>]
```

### Arguments:
*   `--name`: Directory folder name (e.g. `openff_Topology`).
*   `--type`: The type of form (`class`, `file`, or `string`).
*   `--class-name`: For class types, the expected type signature checked in `is_form.py` (e.g., `'openff.toolkit.topology.Topology'`).

This command automatically generates a pristine, fully documented adapter folder under `molsysmt/form/` containing:
1.  `__init__.py`
2.  `is_form.py`
3.  `attributes.py`
4.  `has_attribute.py`
5.  `iterators.py`
6.  `get_topological_attributes.py`
7.  `get_structural_attributes.py`

---

## 6. QA Conformance Linter

To prevent contract drift, regression, or lazy-import leaks, the automated linter performs a structural audit across all 90+ directories in `molsysmt/form/`.

Run the linter locally before committing any new code:
```bash
python devtools/scripts/validate_form_adapters.py
```

### CI/CD Enforcement
The validator runs on every commit. If any adapter misses a contract variable, fails importing due to eager dependencies, or implements non-conforming iterators, the linter exits with code `1`, blocking the build.
