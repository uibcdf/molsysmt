---
summary: Classify rotatable bonds and derive rigid molecular fragments
issue: uibcdf/molsysmt#224
status: resolved
opened: 2026-09-22
closed: 2026-10-04
verification: measured
area: [structure, build]
guard: tests/topology/test_get_rotatable_bonds.py::test_independently_specified_chemical_pairs_and_exclusions
normative: docs/content/user/tools/topology/get_rotatable_bonds.md
blocked_by: []
supersedes: []
---

# Classify rotatable bonds and derive rigid molecular fragments

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Resolved within the bounded graph criteria described below.
Explicit chosen-bond partitioning and native eligibility are implemented and
contract-tested. Consumer active-torsion policy remains separately owned.

## What

Expose reusable torsion candidates and the rigid fragments induced by chosen active bonds.

## How

Classify eligible bonds from chemical graph information, explain exclusions such as rings and amides, then derive connected rigid fragments while preserving source atom and bond IDs.

## Why

Existing covalent-block and dihedral operations do not provide a general small-molecule torsion model needed by a flexible PDBQT ligand writer.

## What is measured and what is assumed

**Inspected:** Inspected topology/get_covalent_blocks.py and structure/get_dihedral_quartets.py; Meeko documents configurable rotatable-bond rules.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Making ROOT/BRANCH records the general torsion representation was rejected because those records are PDBQT-specific.

## Scope and exclusions

Chemical classification and fragment graph; rooted PDBQT serialization belongs to uibcdf/molsysmt#214, protocol selection to DockingMT.

## Acceptance criteria

- Tests distinguish acyclic single bonds, ring bonds, amides, and incomplete bond-order inputs.
- Selected active bonds produce deterministic rigid fragments and atom/bond correspondence; unsupported cases fail explicitly.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#6.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.



## Explicit-cut tool checkpoint — 2026-10-03

`molsysmt.topology.get_rigid_fragments` is a documented experimental general
connectivity tool. It resolves a complete state-specific graph from supported
forms before returning packed int64 fragment memberships, source atom/bond
indices, an atom-to-fragment map and aligned branch endpoint/fragment pairs.
Cuts are explicit source bond indices, deduplicated and range checked. Dative
cuts and original-graph non-bridges fail, including simultaneous ring cuts that
would otherwise disconnect the ring. Isolated atoms and disconnected components
remain represented. Empty arrays have defined shapes. Coordinates and source
chemistry remain unchanged. Standalone ChemicalStates and its typed dictionary
are supported without requiring native Topology or structures.

The implementation uses the existing chemical graph resolver and NetworkX
connectivity/bridge primitives. It has no chemistry perception, PDBQT ROOT
representation, atom typing or implicit chemical storage. The PDBQT writer
reuses this public tool to check supplied trees against complete native graphs.
Contract and form-agnostic tests live in
`tests/topology/test_get_rigid_fragments.py`; its doctest and User Guide/course
explain source indices, completeness and rigidity by explicit graph cuts.

**Remaining:** chemical torsion eligibility, ring/amide and bond-order criteria,
selection policy and explanatory exclusions on representative chemistry. No
heavy-workload measurement or Rust optimization claim is made in this stage.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.

## Native eligibility implementation — 2026-10-04

**Implemented:** `molsysmt.topology.get_rotatable_bonds` is an experimental,
form-agnostic, digested public tool. Two descriptive, versioned criteria operate
on the complete source graph before selecting bonds whose endpoints are both
in the requested atom set. Each bond retains source indices and all applicable
exclusions as uint8 bits. Original frame/state resolution, evaluated scope,
producer versions, bibliography and optional Ackredit metadata are explicit.
No chemical store or torsion-tree store is added.

Both criteria require a single nonaromatic original-graph bridge between heavy
atoms with at least two heavy neighbors, neither incident to a triple bond.
`conjugation_restricted@1` additionally excludes C(=N/O/S)-N/O/S single links;
`acyclic_single@1` retains them. Counts are invariant to indexed versus implicit
H on the same heavy graph. The rule includes formamides but does not apply
tertiary-amide symmetry exceptions, normalize charged resonance/tautomer forms,
remove symmetry-equivalent terminal groups or predict barriers. Graph criteria
need declared elements, complete connectivity and supported bond orders; they
do not certify valence. Unknown aromatic flags need no perception, since ring
edges are excluded by connectivity. Known aromatic bridges contradict the
complete graph. Unsupported elements, dative/query chemistry and missing orders
fail explicitly even with an empty output selection.

General graph/state resolution, validated selection and chemistry-only H5MSM
reading reuse `_chemical_graph`; original-graph bridges reuse NetworkX, and
selected cuts reuse public `get_rigid_fragments`. Native classification imports
no RDKit/Meeko, enumerates no cycles and constructs no atom-pair matrix. Its
graph/arrays occupy storage proportional to atoms and listed bonds; no measured
large-system/RSS or compiled-speed claim is made. Existing conversion providers
remain optional at their form boundaries. An RDKit input is cloned before its
conversion or rich selection can assign properties.

**Inspected:** clean RDKit reference `cbfb37abddcd5b5feeac97d53530ae6be83cac0d`,
`Code/GraphMol/Descriptors/Lipinski.cpp`, and clean Meeko 0.8.0 reference
`1eac18bd6d1111f35f9f1abaa8af502c2668d054`, `meeko/bondtyper.py`. RDKit's
[official descriptor documentation](https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html)
confirms distinct NonStrict/Strict/StrictLinkages policies. Their entire SMARTS
or policy tables are not copied. References identify inspected implementations,
not executed torsion providers or a claim that the criteria were authored there.
The names are descriptive and the exact independently implemented rules above
are the normative contract.

**Contract-tested:** independent butane, terminal, ring, alkene/alkyne,
amide/thioamide/amidine/ester/thioester/formamide, tertiary amide, sulfide,
biphenyl, nitrile, disconnected and isolated-atom controls; selected full-graph
context, source bond reordering, nullable chemical fields, H materialization,
H5MSM/native input parity, typed-empty outputs, invalid chemistry/axes, selected
nonreference/frame-associated states and optional-attribution absence/failure.
A symmetry-equivalent tert-butyl control intentionally differs from RDKit Strict;
count agreement must not become an unqualified equivalence claim.

**Comparison-tested:** four checksummed, untouched original Vina SDF/PDBQT
ligands, using an explicitly selected RDKit SDF input route. The native parser's
bounded dialect support is unchanged. Heavy atoms are independently mapped by
coordinates with a maximum permitted difference of 0.001 angstrom and uniqueness
checks. Restricted candidates count 7/5/2/2 (1IEP/1S63/5X72 P59/P69); exact
source pairs and projected heavy-fragment partitions match the prepared reference
except 1S63's aryl–nitrile 26–27 branch, explicitly excluded by the triple-endpoint
rule. The broader criterion additionally retains 1IEP amide 19–20. Descriptor
counts agree with RDKit Strict only on these four controls; neither Vina
preparation nor descriptor parity is universal scientific ground truth.

The initial focused run passed **43 tests in 22.28 s**. Full scoped regression,
doctests and documentation verification are recorded below.
User Guide Foundations/Toolbox/Cookbook, API discovery, experimental registry and
Master course Module 13 are updated. Course changes are narrative-only;
existing executed code/output cells remain unchanged.

## Remaining consumer ownership

uibcdf/dockingmt#6/#17 select active cuts, including any deliberately different
nitrile/amide rules, and ROOT/TORSDOF/export orientation. uibcdf/dockingmt#33
qualifies the composed preparation; #223 separately owns lossy projection and
charge aggregation. Macrocycle/glue and energetic/symmetry models are outside
this bounded classification. General receiver acceptance is not a condition
for claiming these tested provider criteria are implemented.

## Resolution and verification — 2026-10-04

The reusable eligibility and fragment contracts satisfy this proposal's bounded
acceptance. Future chemical/energetic policy extensions need separate explicit
methods; consumer ROOT, active-cut decisions and lossy export are not certified
by this resolution.

**Measured:** Linux source checkout, Python 3.13.14 under migration exception
uibcdf/molsysmt#237, NumPy 2.4.6 and RDKit 2025.09.5 for the deliberately chosen
reference-input/descriptor tests. The public tool reports its actual NumPy and
NetworkX versions. Released ArgDigest 0.13.0 at
`9880fa7b990fd0987ff0de715b665eb9e11c11b2` supplies the temporary test-path route
because the installed editable snapshot is below the public floor.

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/topology tests/form/file_pdbqt/test_real_vina_examples.py \
  tests/physchem/test_get_aromaticity.py \
  tests/physchem/test_get_autodock_atom_types.py \
  tests/build/test_assign_autodock_atom_types.py --doctest-modules \
  molsysmt/topology/get_rotatable_bonds.py molsysmt/topology/get_rigid_fragments.py
```

This affected-scope run passed **204 tests in 85.82 s**, with twelve expected
legacy H5MSM 0.4 read warnings. A final focused run, including a fresh subprocess
that rejects RDKit/Meeko imports, passed **29 tests in 26.64 s**. The runs overlap;
their totals must not be added as unique tests. Scientific code from the wider
run remains unchanged; the final run adds an independence guard.

The tutorial's Python example executed independently. Parallel Sphinx HTML
compilation succeeds after removing the new page's directive warning. Existing
course/navigation/API-reference debt remains under #144. No new rotatable-bond
page/API warning remains. The maintained course validator passes 156 notebooks;
only Module 13 narrative and function inventory changed, with executed code and
outputs preserved. Ruff lint and format, dependency import audit, 238 public
docstrings, signature guard, 258-symbol registry and developer-guide validation
pass. This is scoped source evidence, not a full suite, interpreter/platform
matrix, clean wheel, large-system performance or biological qualification.

Guards: the front-matter analytical selector; native optional-provider isolation
in `tests/topology/test_get_rotatable_bonds.py`; and original reference pairs/
partitions in `tests/form/file_pdbqt/test_real_vina_examples.py::test_rotatable_source_pairs_preserve_original_vina_policy_differences`.
