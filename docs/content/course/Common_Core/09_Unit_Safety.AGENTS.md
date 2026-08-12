# Module 09 Content Governance (`09_Unit_Safety.AGENTS.md`)

This document defines the **non-negotiable content contract** for `09_Unit_Safety.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Physical Unit Safety** using MolSysMT's integrated unit engine **PyUnitWizard** (`molsysmt.pyunitwizard`).

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).
* **Note:** This module intentionally does **not** include a Glossary box.

### 2. Section 1: Quantity Agnosticism
* Must demonstrate passing physical quantities as strings (e.g. `'[1.0, 4.0, -2.0] angstroms'`) or formal quantity objects into MolSysMT functions like `msm.set()`.
* Must include a hyperlinked reference to the [PyUnitWizard documentation](https://www.uibcdf.org/pyunitwizard) for supported quantity types (Pint, OpenMM, Astropy, etc.).

### 3. Section 2: Inspecting and Converting
* Must demonstrate inspecting quantities using `puw.is_quantity()`, `puw.get_value()`, `puw.get_unit()`, and converting between units using `puw.convert()`.
* Must feature a `:::{note}` admonition inviting users to explore the [PyUnitWizard documentation](https://www.uibcdf.org/pyunitwizard) for advanced unit functions.
* **Note:** This module intentionally omits function `Hint` boxes for PyUnitWizard native functions.

### 4. Section 3: Standard Units
* Must demonstrate configuring global standard units via `puw.configure.set_standard_units()`.

### 5. Section 4: Dimensional Arithmetic
* Must demonstrate dimensional safety in physical arithmetic (e.g. adding distance quantities with compatible dimensions, or trying illegal physical operations).

### 6. Challenge & See Also
* Must include **Challenge 9: The Unit Master**, and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-unit-safety-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 8 and Module 10.
