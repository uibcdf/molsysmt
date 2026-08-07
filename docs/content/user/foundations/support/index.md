(user-foundations-07-support)=
# Support & Coverage

Welcome to **Support & Coverage**, the foundational module detailing MolSysMT's interoperability matrix across in-memory data structures, disk file formats, physical-chemical metadata, and 3D visualization engines.

As a form-agnostic framework, MolSysMT bridges native representations with external computational chemistry tools, ensuring seamless data flow across packages without manual format re-encoding.

---

## **Contents**

- **{doc}`supported_forms`**  
  Matrix of supported native classes (`molsysmt.*`) and third-party in-memory objects (MDTraj, OpenMM, MDAnalysis, ParmEd, PyTraj, BioPython, NetworkX, RDKit).

- **{doc}`supported_files`**  
  Supported disk file formats (`.h5msm`, `.pdb`, `.cif`, `.gro`, `.dcd`, `.xtc`, `.mol2`, `.prmtop`, `.inpcrd`, `.psf`, `.sdf`) and streaming I/O capabilities.

- **{doc}`supported_physchem`**  
  Supported physical-chemical metadata, forcefields (AMBER, CHARMM, GROMOS, OPLS), water models (TIP3P, TIP4P, SPC/E), and implicit solvent models.

- **{doc}`supported_viewers`**  
  Supported 3D rendering backends (MolSysViewer, NGLView, Py3Dmol) and environment compatibility.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   Supported Forms <supported_forms.md>
   Supported Files <supported_files.md>
   Supported Physical-Chemical Metadata <supported_physchem.md>
   Supported Visualization Engines <supported_viewers.md>
```
