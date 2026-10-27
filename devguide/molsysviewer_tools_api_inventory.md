# MolSysViewer tools — expert API inventory and expansion order

**Role:** maintained source inventory and implementation plan under
uibcdf/molsysmt#421 / uibcdf/molsysviewer#264.
**Snapshot:** 2026-10-27, native basis 87a86d439 plus the reviewed remaining
physchem wrappers and initial build diagnostics. This is source exposure, not
installed compatibility, scientific accuracy or unconditional stability.

Regenerate the full path/signature/missing-route inventory in the participating
source environment:

```bash
python devtools/scripts/audit_molsysviewer_tools_api.py \
  --output devtools/data/molsysviewer_tools_api_inventory_20261027.json
```

The command uses real native declarations and an actual empty view's addon,
without calling scientific functions. A missing provider/host cannot silently
be counted as zero. HEAD identifies the checkout basis; the inventory observes
working-tree source too. Local receiving records identify tested code hashes.
Keep historical receipts immutable; a new baseline needs a new dated snapshot.

## Actual function-path exposure

| Namespace | Exposed source paths | Declared native paths | Remaining |
| --- | ---: | ---: | ---: |
| basic | 19 | 26 | 7 |
| topology | 11 | 11 | 0 |
| structure | 28 | 28 | 0 |
| pbc | 13 | 13 | 0 |
| physchem | 34 | 34 | 0 |
| build | 3 | 30 | 27 |
| molecular_mechanics | 0 | 6 | 6 |
| interactions (canonical families) | 0 | 15 | 15 |
| element and declared children | 0 | 57 | 57 |
| h5msm file utilities | 0 | 7 | 7 |
| historical hbonds aliases | 0 | 4 | 4 |

These are 108 exposed out of 231 inspected public function paths. This is not
231 independent scientific capabilities: the historical hbonds routes alias
canonical interaction functions. Constants, classes/methods, form adapters,
configuration, datasets and third-party bridges are outside this functional
inventory. The output records implementation identities so aliases remain
visible rather than inflated into new scientific algorithms. It records
primary, destination-system, explicit-collection and explicit-input contracts;
it does not authorize automatic binding or infer effects from function names.

The zero for addon interactions does not describe Viewer core availability.
`view.interactions` already owns visual calculations/attachment and presentation.
The future expert mirror returns ordinary native scientific results, without
implicitly attaching or representing them. Direct MolSysMT remains available.

## Ordered expansion

1. **Retain the received baseline.** Complete exact-source CI for all 34 physchem
   wrappers and three build diagnostics. Keep the native CIP reference-ownership
   limit uibcdf/molsysmt#503 and source/installed distinctions visible. The prior
   636003965 CI run 40580219002 is failure evidence: the last addon file was a
   shell command rather than a pytest argument. Preserve its completed earlier
   tiers and require a corrected official success, not a relabelled subset.
2. **Finish read-only build diagnostics.** Review missing-atom/bond/group audits,
   supported chemistry and hydrogen/solvation checks before preparation. Each
   function keeps its exact native axes, providers and unsupported outcomes.
   The first three are get_residue_chemical_coverage,
   get_covalent_bond_candidates and get_peptide_bond_candidates. Unknown legacy
   chain metadata remains unassessed; use positive declared-chain systems too.
3. **Expose raw canonical interaction calculations.** Preserve family paths,
   recognition/detection distinctions, sparse participants/roles, evaluated
   scope, units, PBC images and evidence. Do not attach results or override the
   core visualization API. Receive each detector/profile; do not infer that a
   generic interaction wrapper qualifies all scientific families.
4. **Independent outputs and explicit utilities.** Receive basic.compose_atom_maps,
   basic.permute_atoms and collection-composition routes individually. Native
   to/from targets and molecular_systems collections are not automatically the
   current primary. File utilities and element helpers preserve their explicit
   inputs and ownership; some are useful before any system is loaded.
5. **Molecular mechanics calculations.** Start with diagnostics and independently
   returned energies/forces. Keep force field, engine, atom correspondence,
   units, provider availability and preparation prerequisites explicit. Receive
   minimization separately as a potentially mutating operation; no hidden
   parameterization or engine fallback is introduced.
6. **Molecular edits and preparation.** Review every remaining build edit and
   basic add/append/merge route by native effect, return ownership and mapping.
   Independent native outputs may remain independent; in-place operations need
   their own host synchronization, atom/structure correspondence, invalidation,
   retained source identity and recovery contract. Existing coordinate/removal
   receiving does not admit arbitrary topology edits. Public build.editable and
   factories need explicit native object/lifetime contracts, not placeholders.
7. **Complete navigation and compatibility decisions.** Receive element/file
   utilities, canonical versus historical aliases and the basic.view bridge
   deliberately. A useful core route is not proof that its expert mirror exists.
   Review duplicate value and documentation before adding historical aliases.

## Acceptance for each added tool

Use explicit Python methods mirroring the native scientific path/signature, with
the admitted primary implicit and native argument digestion preserved. Validate
real supported systems, nontrivial success and native rejection, axes/units,
independent versus in-place ownership, pending/closed/replacement behavior,
source/scene preservation or supported invalidation, actual provider scope and
provenance. Keep computational assumptions visible. Update native usage guidance
and relevant course modules; Viewer owns addon management/catalogue/authoring.
Graphical tasks cannot narrow the expert API or pretend unreceived tools exist.
A missing native capability/defect belongs to its scientific owner, with linked
consumer evidence. No blanket dynamic forwarding, scientific workaround,
automatic primary observation, hidden preparation or release promise is added.
