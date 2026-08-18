# Core Architecture

Core design principles, lazy loading mechanisms, argument validation, and internal frameworks powering MolSysMT.

---

## Architectural Modules

| Guide | Description |
| :--- | :--- |
| {doc}`dependencies` | Lazy loading architecture and dependency management via DepDigest |
| {doc}`argdigest` | Boundary argument validation and digestion via ArgDigest |
| {doc}`pyunitwizard` | Physical units safety, standard units, and Fast-Track bypass |
| {doc}`element_and_native_rebuild` | Topological element hierarchy and native object rebuild rules |
| {doc}`molsys_builder` | Interactive molecular system builder (`MolSysBuilder`) |
| {doc}`declarative_serialization_forms` | Declarative YAML serialization formats |
| {doc}`new_form` | Step-by-step guide to implementing a new form adapter |
| {doc}`return_types` | Which scalar type a returned container carries, and why |

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   dependencies
   argdigest
   pyunitwizard
   element_and_native_rebuild
   molsys_builder
   declarative_serialization_forms
   new_form
   return_types
```
