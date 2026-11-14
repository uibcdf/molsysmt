# Native membership and correspondence: BindingSite owner contract

**Role:** normative, finite owner disposition under uibcdf/molsysmt#746.
**Consumer:** uibcdf/bindingmt#111, source-index declaration profile at
`e1e6a337dbf487d1b2e36809cc72ea46a7639f60`.
**Review:** 2026-11-13; exact owner source and selected-byte receiving are
recorded in the [receipt](../devtools/data/binding_membership_receiving_746_750_20261113.json).

This offers existing public MolSysMT operations for declared native molecular
membership and correspondence. It does not implement BindingMT's
`resolve_region`, authenticate a molecular source, infer a chemical state or
qualify a current binding finding. No new kernel, matcher, observer, serializer,
universal receipt or dependency floor is introduced. Reuse the applicable
[contacts/SASA map facts](native_interface_contacts_sasa_contract.md); that
separate profile does not qualify this consumer operation.
This disposition adds no release prerequisite beyond the separately admitted
#750 correctness fix; consumer implementation and adoption remain separate.

## Admitted source and scope

The first received source is a resident native MolSys with stable atom/group
inventory and declared, consistent domain axes. Construct native objects with
`from molsysmt.native import MolSys, Structures`, or use the public conversion
route `msm.convert(..., to_form="molsysmt.MolSys")`. A form identifier is not
necessarily a root-package constructor attribute.

Public generic functions remain form agnostic. These checked native facts do
not silently qualify a foreign conversion, lost fields or a new target order.
The caller admits the conversion and retains its relevant correspondence first.

The caller keeps source owner/id/revision declarations, the intended source
and target axes and a consistent snapshot during the operation. An independent
read or copy can help manage that lifecycle but does not authenticate origin.
Counts, labels and well-shaped maps cannot establish that two arbitrary assets
have common origin or that coordinates/chemistry are unchanged. These getters
provide no source/revision attestation or general check/use guarantee.

Stable group membership belongs to Topology. Bonds, assignments and components
belong to ChemicalStates. No topology chemical facade or implicit reconstruction
is used. Declared membership does not certify valence, protonation, physical
completeness, binding relevance or evidence applicability after an edit.

## Public facts, checks, caller preconditions and refusals

| Fact / public route | MolSysMT checks or supplies | Caller precondition / refusal |
| --- | --- | --- |
| `molsys.get(n_atoms=True, n_groups=True, n_structures=True)` | Stored axis cardinalities | Admit a consistent native inventory and required domains. Counts alone do not validate every stored relationship or source identity. |
| `molsys.chemical_states.get(n_chemical_states=True, chemical_state_index=True)` | Stored collection positions, independently of a scientific state choice | Declare which state is applicable; positions and state labels are different. |
| `msm.select(..., element="atom"/"group", selection=indices, structure_indices=chosen)` | Integer index bounds against available axes; explicit numeric order | BindingMT retains its stricter unique declaration contract. Missing axis cardinality is not proof that an index exists. #750 restores structure checks for every selection branch. |
| `molsys.get(element="group", selection=groups, atom_index=True)` | One atom-index list per requested group, in requested group order; atoms within each group follow the stored atom axis | Choose source-member versus current-target-group expansion explicitly. Unknown parentage cannot certify complete expansion. |
| `molsys.get(element="atom", selection=atoms, group_index=True)` | Stored atom-to-group relationships aligned with requested atoms | Preserve missing values and validate required membership. Do not interpret an ID as an index. |
| `molsys.get(structure_indices=chosen, structure_chemical_state_index=True)` | Associated state positions, preserving structure order and repetitions | Compare with the declared scope. Unknown or contradictory required state context refuses the consumer's complete projection. |
| `msm.select(..., chemical_state="structure", structure_indices=[s])` | Resolves the actual associated state for a chemical predicate; missing or mixed-state scope refuses | Choose one occurrence/state or separate per-state calls; do not silently use the reference state. Static inventory facts require no chemical inference. |
| `msm.extract(...)` | Independent selected native domains, sorted unique source atoms and requested structure occurrences | Keep the known extraction correspondence explicitly: this API does not return a general atom/group/structure map report. |
| `msm.permute_atoms(..., return_report=True)` | Complete atom bijection, both atom directions and available labels; preserved other axes and state associations | The experimental report is an atom report, not a group/structure identity certificate. |
| `msm.compose_atom_maps(reports)` | Typed schema, counts, ranges, inverse consistency and available adjacent labels/bindings; explicit omitted/generated atoms | Declare adjacent axis association. Missing/contradictory maps refuse; valid maps do not authenticate origin or current finding. |

Native domain attachment also checks applicable shared atom/structure alignment
before publishing a replacement. That is an operation boundary, not proof that
subsequent arbitrary DataFrame/array edits are valid. Counts remain unchanged
in the received counterexample with unknown parentage or edited coordinates.

## Entry order and explicit expansion

For the received six-atom source, stable group indices by atom are
`[0, 1, 0, 2, 1, 2]`. Atom and group IDs deliberately contain duplicates and
numeric-looking strings; they do not define correspondence.

```python
msm.select(molsys, selection=[5, 1, 2], structure_indices=[2])
# [5, 1, 2]
molsys.get(element="group", selection=[2, 0], atom_index=True)
# [[3, 5], [0, 2]]
molsys.get(element="atom", selection=[3, 5, 0, 2], group_index=True)
# [2, 2, 0, 0]
```

Keep each declared entry and its output list aligned. Queries can repeat atom
positions; BindingMT's current factories instead reject duplicate atom/group
declarations. Expressions such as `group_index in [2, 0]` return the source-
ordered atom set `[0, 2, 3, 5]`. An active mask also returns a sorted set
intersection. Neither result is an ordered group expansion receipt.

A valid empty group can return `[[]]`; an out-of-range group refuses. Unknown
atom parentage remains available as a missing group index even when counts and
the group's expansion look empty. The client must not turn that uncertainty
into certified complete membership or a negative scientific finding.

## Extraction, permutation and group correspondence

Requesting unique atoms `[5, 1, 2]` extracts the output atom order `[1, 2, 5]`.
For that owned operation the caller can declare the following atom-map sidecar:

```python
extraction_map = dict(
    schema="molsysmt.atom_map@1", n_source_atoms=6, n_output_atoms=3,
    source_to_output_atom_indices=[-1, 0, 1, -1, -1, 2],
    output_to_source_atom_indices=[1, 2, 5],
)
subset = msm.extract(molsys, selection=[5, 1, 2], structure_indices=[2, 0, 2])
permuted = msm.permute_atoms(subset, [2, 0, 1], return_report=True)
atom_map = msm.compose_atom_maps([extraction_map, permuted["report"]])
# output_to_source_atom_indices: [5, 1, 2]
# source_to_output_atom_indices: [-1, 1, 2, -1, -1, 0]
```

This sidecar follows a known extraction; it is not a newly generated extraction
report, a matcher or evidence that an arbitrary map is true. There is no need
to physically reorder a molecular asset merely to keep an entry-aligned lookup:
the consumer can retain its declared source order and aligned mapped indices.

Groups in a native atom subset follow first surviving atom occurrence. Here
source group order in the subset is `[1, 0, 2]`, not independently sorted source
groups. Obtain source parents for `[1, 2, 5]` and output parents on the subset's
atom axis; the aligned pairs give `{1: 0, 0: 1, 2: 2}`. The subsequent atom
permutation retains this group axis and yields parents `[2, 0, 1]`.

This derives correspondence for groups supported by surviving atoms of the
known operation. Empty groups or unrelated assets need separately declared
group correspondence and applicable checks; do not guess from equal labels.
Historical preparation maps keep their original operation domains and must
not be mistaken for current local axes after further edits.

## Repeated structure occurrences and chemical states

Keep an explicit occurrence table, separate from the one-to-one atom maps:

| Declaration occurrence | Source structure index | Target-local structure index | Associated state index in the received example |
| --- | --- | --- | --- |
| 0 | 2 | 0 | 0 |
| 1 | 0 | 1 | 1 |
| 2 | 2 | 2 | 0 |

The source-to-target structure relation is `[[1], [], [0, 2]]`. A scalar inverse
map would lose one occurrence of source structure 2. `compose_atom_maps` does
not compose a structure relation. The extraction request supplies the known
structure correspondence; source and target association getters check its
declared state context. No independent repetition, frequency weight or evaluated
realization follows from the repeated reference.

State collection order is preserved, while structure-to-state associations are
selected in requested order. The receiving exercises distinct stored charge
assignments and the associated predicate after permutation and H5MSM readback,
under nm/ps and pm/fs policies. Read quantity values with an explicit target
unit, for example `puw.get_value(coordinates, to_unit="nm")`.

The caller distinguishes structure-independent membership from explicitly
chosen source occurrences. Do not turn an unspecified declaration into all
structures/states. For a state-dependent query, choose an explicit integer
state or the associated state of one explicitly chosen structure. A mixed-state
request cannot yield one ordinary chemical atom selection and refuses; absent
association remains unknown. No reference state is chosen as a substitute.

## Missing, partial, contradictory and generated members

Check required source members against the validated forward map **before any
target lookup**. `-1` is absence, never a Python last-element index. In the
example, source requests `[0, 5]` map to `[-1, 0]` after permutation: atom 0 is
omitted, while atom 5 survives at target 0. Complete coverage must refuse an
omission. An explicitly admitted partial BindingMT profile may retain the
omissions, reason, original declaration and weaker guarantee; MolSysMT's map
composition does not decide that application policy.

Missing maps are not identity maps. Unknown schemas, invalid ranges, conflicting
inverse directions and incompatible adjacent counts/available labels refuse.
Schema-valid partial maps can still be scientifically inappropriate or declared
against the wrong asset; the caller owns that association.

An actual `msm.build.add_terminal_atoms` control changes a current group's
members from `[0]` to `[0, 1]`. Its composable report marks target atom 1 with
inverse index `-1` and lists it as generated. A declaration by original atom
membership still refers to original atom 0 only. An explicit current-group
expansion can include the generated atom, while retaining its absent original
atom identity. Parent membership does not transmit an old observation, support
or confidence to the new atom. Those are BindingMT evidence semantics.

## Persistence, source disposition and remaining work

The molecular receiving writes and publicly reads a small H5MSM system after
extraction/permutation, preserving the tested atom/group/state/coordinate axes.
The atom-map sidecar and BindingSite source/occurrence declarations are retained
explicitly by the caller; this does not add a native BindingSite domain or
automatic persistence of arbitrary sidecars. Saved BindingMT data-only replay
and the actual `resolve_region` result remain BindingMT responsibilities.

**Owner disposition:** existing public routes supply the finite molecular
facts for the admitted declared-membership profile. #750 repairs the concrete
selection-boundary defect found by this review. No other new molecular operation
gap is established by the received cases. Unproved source authentication,
automatic revision/current-finding validity and undeclared cross-asset matching
are not offered. C2 geometry/domain application, universal observers and sibling
adoption are outside this disposition.

The meaningful new guard is
`tests/basic/test_binding_site_membership_handoff.py`. The #750 guard is
`tests/basic/select/test_structure_scope.py`; the receipt names reused map,
native-query, state-association and #734 controls. Synthetic chemical values
test transport and scope, not realistic valence or binding science. No new
third-party scientific method or attribution boundary is introduced.

BindingMT must review and qualify its real composition on compatible source/
native/runtime inputs. Its existing `e1e6a337` declaration-only receiving is
not molecular adoption of these facts. MolSysMT's local tests are not clean
installed/platform/final-pair qualification or a publication authorization.
