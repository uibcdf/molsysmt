(user-foundations-support-physchem)=
# Physical-Chemical Data

MolSysMT standardizes physical-chemical properties, atomic attributes, element classifications, biophysical scales, and volumetric observables across diverse structural chemistry models and software packages.

---

## Atomic Properties

Properties describing individual atoms, elements, isotopes, and core physical invariants:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`atom_name`** | Atom | IUPAC/PDB atom identifier string (e.g., `"CA"`, `"N"`, `"OG"`). | N/A |
| **`atom_type`** | Atom | Canonical chemical element symbol, such as `C`, `N`, `O` or `Fe`. | N/A |
| **`element_symbol`** | Atom | External spelling in some libraries; MolSysMT uses `atom_type` for this meaning. | N/A |
| **`atomic_number`** | Atom | Nuclear proton count ($Z$). | N/A |
| **`mass`** | Atom / Group / System | Atomic, residue, or total molecular system mass. | `dalton` (`Da`) |
| **`isotope`** | Atom | Isotope mass number ($A$). | N/A |
| **`atomic_radius`** | Atom | Supported van der Waals or ProtOr radius for an atom. | `nanometer` (`nm`) |

---

## Chemical State and Charges

Properties defining electronic states, formal/partial charges, and protonation:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`charge`** | Atom / Group / System | Tabulated group scores or OpenMM mechanical charge; distinct from stored formal charge. | `elementary_charge` (`e`); Collantes ECI interpretation under review in #475 |
| **`partial_charge`** | Atom | Forcefield-assigned fractional point charge. | `elementary_charge` (`e`) |
| **`formal_charge`** | Atom / Group | Integer electronic formal charge state. | `elementary_charge` (`e`) |
| **`electronegativity`** | Atom | Pauling atomic electronegativity; unavailable tabulated elements return NaN. | N/A |
| **`aromaticity`** | Atom / Bond | Huckel aromaticity classification flag. | Boolean |
| **`n_implicit_hydrogens`** | Atom | Implicit hydrogen count in the declared chemical graph. | Integer |
| **`n_explicit_hydrogens`** | Atom | Atom-level hydrogen annotations such as RDKit bracket H counts; these do not add indexed H atoms. | Integer |
| **`n_unpaired_electrons`** | Atom | Radical or free electron count. | Integer |
| **`pka`** | Group | Acid dissociation constant value for ionizable groups. | N/A |

Stored H counts describe virtual annotations. Existing H atoms have their own indices
and covalent bonds; counts are not their coordinates. Inspect both with
{ref}`Tutorial_Hydrogen_Inventory`, and explicitly materialize a chosen state using
{ref}`Tutorial_Fixed_State_Hydrogens`. That operation retains the existing pose and
does not predict a pH-dependent state or optimize the receptor environment.

---

## Biophysical and Residue Scales

Property queries honor both the requested selection syntax and their supported
population. Atomic radius (including ProtOr) and Pauling electronegativity accept
only the atom axis. Hydrophobicity, polarity and transmembrane tendency accept
only the group axis. The tabulated surface-area, buried-area and buried-fraction
readers likewise accept only groups. `get_volume` has a fixed group axis and no
element argument. `get_area_buried` has no syntax argument; resolve alternate
syntax with `msm.select` and supply numeric group indices. Unsupported levels fail before interpreting selection;
no sum or mean is invented. Tabulated charge retains its documented group and
higher-level aggregation rules. A group index and an atom index are different
positions even if their integer values coincide.

Explicit index lists retain order and repetitions; empty supported selections
retain the result container and a zero-length axis. String selections use your
specified syntax; MDTraj syntax requires that optional provider. Unknown
non-placeholder group names retain explicit table errors. These queries do not
assign ChemicalStates or certify molecular preparation.


Properties defining residue-level hydrophobicity, polarity, and structural classification:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`group_type`** | Group | Group classification (`amino_acid`, `nucleic_acid`, `water`, `ion`, `small_molecule`, `saccharide`, `lipid`). | N/A |
| **`amino_acid_type`** | Group | Standard 3-letter or 1-letter amino acid code. | N/A |
| **`nucleic_acid_type`** | Group | Standard nucleotide base classification code (`A`, `C`, `G`, `T`, `U`). | N/A |
| **`hydrophobicity`** | Group | Hydrophobicity score from Eisenberg, Kyte-Doolittle or the documented alternative scales. | N/A |
| **`polarity`** | Group | Amino acid sidechain polarity index. | N/A |
| **`transmembrane_tendency`** | Group | Zhao or Senes transmembrane propensity score. | dimensionless |

---

## Surface Accessibility and Volumetric Observables

Observables describing spatial extent, solvent exposure, and molecular volume:

| Attribute / Property | Target Scope | Description | Canonical Unit |
| :--- | :--- | :--- | :--- |
| **`sasa`** | Supported geometric population | Coordinate-based solvent-accessible surface area. | `nanometer ** 2` (`nm²`) |
| **`surface_area`** | Group | Raw tabulated Collantes descriptor; physical unit review remains open in issue #473. | unqualified raw values |
| **`volume`** | Group / System | Molecular or atomic volume via Voronoi tessellation or solvent envelope. | `nanometer ** 3` (`nm³`) |
| **`area_buried`** | Group / Interface | Surface area buried upon interface formation or folding. | `nanometer ** 2` (`nm²`) |
| **`buried_fraction`** | Atom / Group | Fractional extent of surface burial ($0.0 \dots 1.0$). | N/A |

The historical Collantes ISA table is a lookup of QSAR descriptors, not a new
surface measurement on the selected coordinates. Its raw floats do not imply
dimensionlessness or authorize assigning nm² or Å². The original table unit
and normalization remain under [review #473](https://github.com/uibcdf/molsysmt/issues/473).
The companion electronic charge index (ECI), exposed by the legacy Collantes
charge definition, has a separate [unit and aggregation review #475](https://github.com/uibcdf/molsysmt/issues/475).
See the [ISA tutorial](../../tools/physchem/get_surface_area.ipynb) for the
original reference and the distinct coordinate-based SASA route.

Coordinate-based SASA uses Shrake–Rupley sphere sampling, followed by output
selection or aggregation. All atoms in the input remain occluders. Its quantity
is standardized to the square of the configured standard length unit (nm² by
default), independently of coordinate or probe input units. Use explicit area
conversion for exports and comparisons.

Request Cartesian screening with `pbc=False`. With a box, the native default
`pbc=True` uses minimum-image screening by other atoms, excluding self-images;
without a box it is Cartesian. This is not a general all-images surface for
arbitrarily small cells. MDTraj supports Cartesian SASA only and rejects
`pbc=True` with a box. See {ref}`Tutorial_Get_sasa` for examples and sampling
controls. Engine agreement under different boundary conditions does not
establish surface accuracy.

Stored-chemistry readiness keeps the semantic reference-state request when
resolving rich atom selections. External syntax can therefore select atoms in
the default reference without an implicit integer-state override. Explicit and
structure-associated state requests retain the public selector's restrictions.
See {ref}`Tutorial_Chemical_Readiness` for the supported forms and numeric scopes.

Chemical-graph readers preserve a default reference request when delegating to
external selection syntax. Explicit or structure-associated states retain the
common selector restrictions. Ring readers also validate explicit structure
indices on the original source axis; chemistry-only objects use `all` or `None`.
These checks neither infer aromaticity from geometry nor attach ring interactions.
