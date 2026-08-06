(user-foundations-03-native-world)=
# The Native World

Welcome to **The Native World**, the architectural home of MolSysMT's native object representations, containers, data dictionaries, file handlers, and storage formats. While MolSysMT seamlessly interoperates with dozens of third-party libraries and external file formats, its core engine relies on native data structures designed for high flexibility, fast querying, and lossy-free serialization.

The 15 native forms in MolSysMT are organized below into three primary categories: **Classes**, **Files**, and **File Handlers**.

---

## Classes

- **{doc}`molsysmt_MolSys`**  
  The native unified molecular system class composing topology, structures, and molecular mechanics contracts.

- **{doc}`molsysmt_MolSysBuilder`**  
  The editable native container for incrementally constructing and modifying molecular models.

- **{doc}`molsysmt_MolSysDict`**  
  The declarative, serializable dictionary representation of a complete molecular system.

- **{doc}`molsysmt_Topology`**  
  The native topology data structure managing atom inventories, residue groups, and chemical state attributes.

- **{doc}`molsysmt_TopologyDict`**  
  The declarative, serializable dictionary representation of molecular topology.

- **{doc}`molsysmt_Structures`**  
  The native structures data container storing 3D atomic coordinates, periodic boxes, and trajectory frames.

- **{doc}`molsysmt_StructuresDict`**  
  The declarative, serializable dictionary representation of structural and trajectory data.

- **{doc}`molsysmt_MolecularMechanics`**  
  The native molecular mechanics object managing force field terms, partial charges, masses, and energy parameters.

- **{doc}`molsysmt_MolecularMechanicsDict`**  
  The declarative, serializable dictionary representation of molecular mechanics parameters.

- **{doc}`molsysmt_ViewerJSON`**  
  The lightweight, JSON-serializable graphics representation for 3D visualization and web renderers.

---

## Files

- **{doc}`file_h5msm`**  
  The native HDF5-based binary file format designed for rapid I/O, trajectory chunking, and full metadata persistence.

---

## File Handlers

- **{doc}`molsysmt_H5MSMFileHandler`**  
  The low-level native streaming handler for reading and writing H5MSM files.

- **{doc}`molsysmt_PDBFileHandler`**  
  The native file handler for reading and writing Protein Data Bank (PDB) formatted files.

- **{doc}`molsysmt_CIFFileHandler`**  
  The native file handler for reading and writing Macromolecular Crystallographic Information Files (mmCIF).

- **{doc}`molsysmt_GROFileHandler`**  
  The native file handler for reading and writing GROMACS GRO structure files.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   molsysmt.MolSys <molsysmt_MolSys.ipynb>
   molsysmt.MolSysBuilder <molsysmt_MolSysBuilder.ipynb>
   molsysmt.MolSysDict <molsysmt_MolSysDict.ipynb>
   molsysmt.Topology <molsysmt_Topology.ipynb>
   molsysmt.TopologyDict <molsysmt_TopologyDict.ipynb>
   molsysmt.Structures <molsysmt_Structures.ipynb>
   molsysmt.StructuresDict <molsysmt_StructuresDict.ipynb>
   molsysmt.MolecularMechanics <molsysmt_MolecularMechanics.ipynb>
   molsysmt.MolecularMechanicsDict <molsysmt_MolecularMechanicsDict.ipynb>
   molsysmt.ViewerJSON <molsysmt_ViewerJSON.ipynb>
   file:h5msm <file_h5msm.ipynb>
   molsysmt.H5MSMFileHandler <molsysmt_H5MSMFileHandler.ipynb>
   molsysmt.PDBFileHandler <molsysmt_PDBFileHandler.ipynb>
   molsysmt.CIFFileHandler <molsysmt_CIFFileHandler.ipynb>
   molsysmt.GROFileHandler <molsysmt_GROFileHandler.ipynb>
```
