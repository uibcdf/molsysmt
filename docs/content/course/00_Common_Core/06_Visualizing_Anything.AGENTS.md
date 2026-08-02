# Module 06 Content Governance (`06_Visualizing_Anything.AGENTS.md`)

This document defines the **non-negotiable content contract** for `06_Visualizing_Anything.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module presents **Form-Agnostic Molecular Visualization** using MolSysMT's unified `msm.view()` engine.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block & Glossary
* Must feature the **Glossary: Visualization** admonition (````{admonition} Glossary: Visualization\n:class: dropdown info`) with an active cross-reference link to `{ref}`user-foundations``.
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Remote & Cloud Systems (`msm.view('pdb_id:')`)
* Must demonstrate rendering remote database entries directly using `msm.view('pdb_id:6LU7')`.

### 3. Section 2: Local Files & Native Objects (`msm.view(system)`)
* Must demonstrate rendering local files and native `molsysmt.MolSys` objects (`lysozyme`).
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.basic.view``.

### 4. Section 3: Multi-Forms & Trajectories (`msm.view([topology, trajectory])`)
* Must demonstrate rendering composite multi-form lists (e.g. `[topology, trajectory]`) and trajectory animation controls.

### 5. Section 4: Selective Focus & Viewer Backends
* Must demonstrate focusing view on specific components using basic `selection` arguments.
* Must note that selection syntax is explored in depth in Module 7 and Module 8.

### 6. Challenge & See Also
* Must include **Challenge 6: The Scene Director** using Barnase-Barstar (`systems['Barnase-Barstar']['barnase_barstar.h5msm']`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-06-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 5 and Module 7.
