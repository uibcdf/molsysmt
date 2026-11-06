(user-foundations-03-native-world)=
# The Native World

Welcome to **The Native World**, the architectural home of MolSysMT's native object representations, containers, data dictionaries, file handlers, and storage formats. While MolSysMT seamlessly interoperates with dozens of third-party libraries and external file formats, its core engine relies on native data structures designed for high flexibility, fast querying, and lossy-free serialization.

The 15 native forms in MolSysMT are organized below into three primary categories: **Classes**, **Files**, and **File Handlers**.

Logical independence does not always require duplicating numeric bytes. An
`Interactions` copy owns independent mutable metadata and array headers while
sharing proven immutable storage. Its query selection and evaluated coverage
remain intact, including lazy invalidation and replacement. Python deep copies
preserve repeated analysis references and cycles through one copy memo. These
guarantees are specific to the analysis object; shared-storage copying of a
complete molecular system is still under development. See
{ref}`Copying analyses <user-tools-interactions-copying>` for the raw-column
ordering boundary and practical examples.

---

## **Contents**

A native molecular projection and a format-preserving document edit serve
different purposes. A prepared PDBQT can carry mechanical labels, charge
precision and a torsion tree that do not amount to complete native chemistry.
Its experimental handler can replace explicitly mapped coordinates while
retaining those prepared fields, with declared metadata losses and independent
output. This neither fills missing atoms nor certifies a chemical state.
See {ref}`Tutorial_Project_Prepared_PDBQT` for that representation boundary.

- **{doc}`classes/index`**  
  Native Python classes and declarative dictionaries representing molecular systems, topology, structures, molecular mechanics, and visualization schemas.

- **{doc}`files/index`**  
  Native file formats developed for high-performance storage and trajectory streaming.

- **{doc}`file_handlers/index`**  
  Low-level native streaming handlers for reading and writing molecular file formats.

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   classes/index
   files/index
   file_handlers/index
```
