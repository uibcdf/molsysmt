(user-foundations-02-molecular-system)=
# The Molecular System

Welcome to **The Molecular System**, the conceptual heart of MolSysMT. This section defines the constitutional architecture of molecular models: how systems are formally defined, how physical items differ from data representation forms, and how orthogonal elements and attributes are structured.

Understanding these foundational concepts ensures seamless interoperability when handling structures across different file formats, computational engines, and external libraries.

Group labels and chemical assignments have different roles. An N-terminal cap
protects the peptide N end: ACE connects through its carbonyl C. C-terminal
NME/NHE/NH2 caps connect through N to the peptide C end. Likewise, sequence
symbols XLE/J and XAA/X retain ambiguous or unknown identity; recognizing a
label does not select a chemical state or provide an atomic template.

Reference-template helpers likewise use explicit names rather than the system's
stored chemical graph. A returned bond-pair endpoint is a local name position
unless you supply a parallel atom-index map. Neither lookup nor mapping assigns
chemical state or modifies the system. See
{ref}`Tutorial_Get_bonded_atom_pairs` for flat list/tuple/NumPy inputs and their
family-specific lookup limits.

---

## **Contents**

- **{doc}`the_molecular_system`**  
  Core definition of a molecular system and the form-agnostic architecture of MolSysMT.

- **{doc}`forms`**  
  Understanding physical molecular items and the catalog of supported data representation forms.

- **{doc}`elements`**  
  The orthogonal structural hierarchy: atoms, groups, components, chains, molecules, entities, and bioassemblies.

- **{doc}`attributes`**  
  Detailed guide to structural, topological, mechanical, and physicochemical molecular attributes.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   The Molecular System <the_molecular_system.md>
   Items and Forms <forms.ipynb>
   Elements <elements.ipynb>
   Attributes <attributes.ipynb>
```
