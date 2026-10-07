(user-foundations-index)=
# Foundations

Welcome to the **Foundations** of MolSysMT. This section introduces the core principles, architectural invariants, and high-performance design that enable MolSysMT to operate seamlessly across different molecular structures, file formats, and computational tools.

Rather than treating molecular systems as rigid data structures bound to a specific software package, MolSysMT builds a form-agnostic bridge. Here you will learn how systems are defined, how physical units and quantities are safely enforced, how selection syntaxes are interpreted, and how native representations ensure speed and interoperability across the structural biology ecosystem. Explore the 8 pillars below to master the underlying framework.

---

## **Sections**

::::{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} **The Entrance**
:link: entrance/index
:link-type: doc

Mission, installation, documentation navigation, toolbox overview, and demo systems.
:::

:::{grid-item-card} **The Molecular System**
:link: molecular_system/index
:link-type: doc

Universal definition of molecular systems, forms, items, elements, and physical attributes.
:::

:::{grid-item-card} **The Native World**
:link: native_world/index
:link-type: doc

Native object classes, topology data, H5MSM trajectory storage, and file handlers.
:::

:::{grid-item-card} **The Language**
:link: language/index
:link-type: doc

Syntactic modes, declarative selection queries, and core API function patterns.
:::

:::{grid-item-card} **Performance**
:link: performance/index
:link-type: doc

Zero-copy array views, chunked execution for large trajectories, and Rust acceleration.
:::

:::{grid-item-card} **Governance**
:link: governance/index
:link-type: doc

Physical units, ArgDigest boundary safety, DepDigest lazy loading, and SMonitor diagnostics.
:::

:::{grid-item-card} **Supported**
:link: support/index
:link-type: doc

Compatibility matrix across data forms, physical-chemical scales, syntaxes, and bridges.
:::

:::{grid-item-card} **The Ecosystem**
:link: ecosystem/index
:link-type: doc

MolSysSuite overview, biophysics tools, and developer software engineering infrastructure.
:::

::::

```{toctree}
:maxdepth: 2
:hidden:

entrance/index.md
molecular_system/index.md
native_world/index.md
language/index.md
performance/index.md
governance/index.md
support/index.md
ecosystem/index.md
```

--- 

```{key-takeaway}
Foundations are the difference between using a tool and mastering an ecosystem. Every API choice follows these 8 pillars.
```
