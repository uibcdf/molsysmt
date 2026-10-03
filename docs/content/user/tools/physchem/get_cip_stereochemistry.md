(Tutorial_Get_CIP_stereochemistry)=
# Getting CIP stereochemistry

*Analyzing absolute chemical configurations without changing your system.*

Use `msm.physchem.get_cip_stereochemistry()` to analyze a supported chemical
source: a native system, an RDKit molecule or a single SDF record. The selected
state must supply chemical element symbols, complete connectivity, explicit
formal charges and supported bond orders. Atom types mean element symbols;
force-field atom types cannot replace them.

:::{admonition} API documentation
{func}`molsysmt.physchem.get_cip_stereochemistry`
:::

## Scientific method and provider

The method is `hanson_2018`, implementing the CIP algorithm described by
[Hanson et al. (2018)](https://doi.org/10.1021/acs.jcim.8b00324).
The explicit optional provider is `engine='rdkit'`, using its accurate
`rdCIPLabeler`, rather than its older approximate label assignment.
Missing RDKit raises a dependency error. There is no silent fallback.

```python
import molsysmt as msm
from rdkit import Chem

molsys = Chem.MolFromSmiles('N[C@@H](C)C(=O)O')
report = msm.physchem.get_cip_stereochemistry(molsys, selection=[1])
assert report['atom_indices'].tolist() == [1]
assert report['atom_stereochemistry'].tolist() == ['S']
```

The full graph is analyzed before selection. Returned indices belong to the
source atom and bond axes; selecting one center does not truncate the branches
needed to rank its substituents. Selection is deduplicated and sorted. Bonds
are returned only when both endpoints belong to the selection. Empty arrays
retain explicit shapes and dtypes. No assigned label is represented by `None`;
it does not establish that an unspecified center is achiral.

## Reference atoms and geometry

Atom labels include R/S and pseudoasymmetric r/s. Double-bond labels use
absolute E/Z. `bond_stereo_atom_indices` names two source reference atoms;
`bond_reference_stereochemistry` describes cis/trans relative to those atoms.
The reference atoms are not promised to be the highest-priority substituents.
Do not substitute the relative label for E/Z.

The default interprets declared stereo. SDF interpretation also follows the
source's supported 2D wedge or 3D CTAB representation. To infer stereo from
native coordinates, opt in with `from_coordinates=True` and select exactly
one structure using `structure_indices=[index]`. The computation uses a copy,
converts lengths explicitly to angstroms through PyUnitWizard and does not
change stored chemical assignments. It does not reconstruct periodic molecules;
provide compatible compact coordinates first. Degenerate geometry may leave
centers unassigned. Multiple selected structures are an error.

## Provenance and supported scope

The detached dictionary retains method, provider, evidence, original software
versions and bibliographic records. When Ackredit is available, successful
analysis contributes to the application's current session, including evaluated
empty selections. Reading the dictionary does not register another calculation.
The result and its bibliography remain available without Ackredit.

The experimental contract covers tetrahedral atom and double-bond descriptors.
Query, enhanced stereo, non-tetrahedral descriptors and parity-only encodings
without a supported wedge or 3D interpretation are rejected. The function does
not return a general CIP priority table or enumerate stereoisomers.

:::{seealso}
{ref}`cookbook-native-sdf` for explicitly enabling stereo in SDF conversion.
:::
