(user-foundations-support-forms)=
# Forms

Welcome to **Forms**, the foundational matrix detailing all object, file, and string data representations supported by MolSysMT.

MolSysMT recognizes forms from declared metadata and confirms a candidate with
its adapter. A conversion loads the adapters needed by its route; it does not
initialize every supported format first. The first use of another adapter may
still have an initialization cost. Listing the complete callable capabilities
can load additional adapters, and inspecting an optional format does not enable
calculations when its required engine is absent.

---

## Contents

- **{doc}`classes`**  
  Supported in-memory object classes across native containers and third-party libraries.

- **{doc}`files`**  
  Supported disk file forms, extensions, and streaming capabilities.

- **{doc}`strings`**  
  Supported string representations, database IDs, chemical SMILES, and sequences.

```{toctree}
:maxdepth: 1
:hidden:

classes
files
strings
```
