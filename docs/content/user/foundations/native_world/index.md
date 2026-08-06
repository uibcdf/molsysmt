(user-foundations-03-native-world)=
# The Native World

Welcome to **The Native World**, the architectural home of MolSysMT's native object representations and storage formats. While MolSysMT seamlessly interoperates with dozens of third-party libraries and file formats, its internal power stems from native data structures optimized for flexibility, fast querying, and high-performance serialization.

This module introduces the primary native container `molsysmt.MolSys`, the dedicated topological model `molsysmt.Topology`, the high-performance HDF5 binary format `file:h5msm`, and the lightweight 3D graphics view schema `molsysmt.ViewerJSON`.

---

## **Contents**

- **{doc}`molsysmt_MolSys`**  
  The native unified molecular system class composing topology, structures, and molecular mechanics contracts.

- **{doc}`molsysmt_Topology`**  
  The native topology data structure managing atom inventories, residue groups, and chemical state attributes.

- **{doc}`file_h5msm`**  
  The native HDF5-based binary file format designed for rapid I/O, trajectory chunking, and full metadata persistence.

- **{doc}`molsysmt_ViewerJSON`**  
  The lightweight, JSON-serializable graphics representation for 3D visualization and web renderers.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   molsysmt.MolSys <molsysmt_MolSys.ipynb>
   molsysmt.Topology <molsysmt_Topology.ipynb>
   file:h5msm <file_h5msm.ipynb>
   molsysmt.ViewerJSON <molsysmt_ViewerJSON.ipynb>
```
