(user-foundations-support-physchem)=
# Physical-Chemical Data

MolSysMT standardizes physical-chemical properties, atomic attributes, element classifications, biophysical scales, and volumetric observables across diverse structural chemistry models and software packages.

---

## Atomic Properties

Properties describing individual atoms, elements, isotopes, and core physical invariants:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`atom_name`** | Atom | IUPAC/PDB atom identifier string (e.g., `"CA"`, `"N"`, `"OG"`). | N/A |
| **`atom_type`** | Atom | Forcefield-specific or ProTor atom type code. | N/A |
| **`element_symbol`** | Atom | Chemical element symbol (e.g., `"C"`, `"N"`, `"O"`, `"Fe"`). | N/A |
| **`atomic_number`** | Atom | Nuclear proton count ($Z$). | N/A |
| **`mass`** | Atom / Group / System | Atomic, residue, or total molecular system mass. | `dalton` (`Da`) |
| **`isotope`** | Atom | Isotope mass number ($A$). | N/A |
| **`atomic_radius`** | Atom | Van der Waals radius, covalent radius, or ProTor VdW radius. | `nanometer` (`nm`) |

---

## Chemical State and Charges

Properties defining electronic states, formal/partial charges, and protonation:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`charge`** | Atom / Group / System | Formal or net electric charge calculated across elements. | `elementary_charge` (`e`) |
| **`partial_charge`** | Atom | Forcefield-assigned fractional point charge. | `elementary_charge` (`e`) |
| **`formal_charge`** | Atom / Group | Integer electronic formal charge state. | `elementary_charge` (`e`) |
| **`electronegativity`** | Atom | Pauling or Mulliken atomic electronegativity scale value. | N/A |
| **`aromaticity`** | Atom / Bond | Huckel aromaticity classification flag. | Boolean |
| **`n_implicit_hydrogens`** | Atom / Group | Count of non-explicitly modeled hydrogen atoms. | Integer |
| **`n_unpaired_electrons`** | Atom | Radical or free electron count. | Integer |
| **`pka`** | Group | Acid dissociation constant value for ionizable groups. | N/A |

---

## Biophysical and Residue Scales

Properties defining residue-level hydrophobicity, polarity, and structural classification:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`group_type`** | Group | Residue classification (`amino_acid`, `nucleic_acid`, `water`, `ion`, `small_molecule`, `saccharide`, `lipid`). | N/A |
| **`amino_acid_type`** | Group | Standard 3-letter or 1-letter amino acid code. | N/A |
| **`nucleic_acid_type`** | Group | Standard nucleotide base classification code (`A`, `C`, `G`, `T`, `U`). | N/A |
| **`hydrophobicity`** | Group | Hydrophobicity score (Kyte-Doolittle, Eisenberg, or Wimley-White scales). | N/A |
| **`polarity`** | Group | Amino acid sidechain polarity index. | N/A |
| **`transmembrane_tendency`** | Group | Free energy scale of insertion into lipid bilayers. | `kilojoule_per_mole` (`kJ/mol`) |

---

## Surface Accessibility and Volumetric Observables

Observables describing spatial extent, solvent exposure, and molecular volume:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`sasa`** / **`surface_area`** | Atom / Group / System | Solvent Accessible Surface Area (Lee-Richards or Shrake-Rupley algorithms). | `nanometer ** 2` (`nm²`) |
| **`volume`** | Group / System | Molecular or atomic volume via Voronoi tessellation or solvent envelope. | `nanometer ** 3` (`nm³`) |
| **`area_buried`** | Group / Interface | Surface area buried upon interface formation or folding. | `nanometer ** 2` (`nm²`) |
| **`buried_fraction`** | Atom / Group | Fractional extent of surface burial ($0.0 \dots 1.0$). | N/A |
