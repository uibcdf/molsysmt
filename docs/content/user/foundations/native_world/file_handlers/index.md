(user-foundations-native-world-file-handlers)=
# File Handlers

Native I/O handlers provide different access and ownership contracts. Some
load text and parsed records into memory; others support indexed or binary
access. Choose by the documented capabilities, not the class name.

---

## Contents

- **{doc}`molsysmt_PDBFileHandler`**  
  Resident reader for Protein Data Bank (`.pdb`) records; its live-handler
  writing, copying and form-specific streaming routes are unavailable.
- **{doc}`molsysmt_H5MSMFileHandler`**  
  Legacy 0.3/0.4 HDF5 handle manager with supported query/iteration routes;
  modular 0.5/0.6/1.0 uses separate public resident/layer APIs.
- **{doc}`molsysmt_GROFileHandler`**  
  Resident first-entry reader for GROMACS GRO (`.gro`) files.

```{toctree}
:maxdepth: 1
:hidden:

molsysmt_PDBFileHandler
molsysmt_H5MSMFileHandler
molsysmt_GROFileHandler
```

The experimental {ref}`PDBQTFileHandler <Tutorial_Form_PDBQTFileHandler>`
provides resident and indexed modes for PDBQT pose ensembles, with explicit
source-consistency and iterator-ownership limits. See its existing guide and
{ref}`native PDBQT workflows <cookbook-native-pdbqt>` before choosing a mode.
