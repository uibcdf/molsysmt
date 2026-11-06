(Tutorial_Infer_Covalent_Bonds)=
# Infer covalent bonds

*Applying bounded native candidates while retaining their scientific evidence.*

Use {func}`molsysmt.build.infer_covalent_bonds` to apply the supported candidate
policies to a detached `MolSys`. The source form can be native, a PDB or another
supported form with names, elements and group membership. The source stays
unchanged, including on failure.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

See {func}`molsysmt.build.infer_covalent_bonds` for arguments and errors.
:::

## Applying a declared policy

```python
result = msm.build.infer_covalent_bonds(
    molsys, structure_indices=0, return_report=True,
)
prepared = result['molecular_system']
report = result['report']
```

The experimental `supported_group_templates` method composes existing public
tools rather than a new parser-specific chemistry engine:

- {ref}`Exact heavy-group templates <Tutorial_Covalent_Bond_Candidates>`.
- Exact-name local consensus on the heavy parent of each **already observed H**.
- {ref}`Unique same-chain peptide C-N geometry <Tutorial_Peptide_Bond_Candidates>`.

Choose `method='supported_group_templates_with_hydrogen_aliases'` to use the
explicit H-name alternative from the same public candidate tool. Heavy templates,
peptide geometry, source ownership and invalidation rules are unchanged. This
alternative records the pinned name dataset and detached bibliography under
`hydrogen_name_policy`, including in H5MSM history. It does not rename atoms,
interpret group-name aliases, import OpenMM, select protonation or establish
stereochemical H roles. The default method keeps exact H-name matching. See
{ref}`Tutorial_Covalent_Bond_Candidates` for alias scope and exclusions.

Only missing eligible pairs are appended as `type='covalent'` and
`evidence='inferred'`. Orders remain unknown. Existing rows and their declared
types, orders and evidence are retained. Both endpoints must be selected, but
containing groups and backbone competitors are examined before filtering.
Selections restrict additions; they do not extract the source atom inventory.

Choose one structure when several exist. The whole source structure collection
is retained. A topology without coordinates can supply template edges, while
peptide geometry remains unassessed. Geometry uses `pbc=False` and the bounded
0.153 nm effective ceiling. This operation can materialize/copy coordinates;
it is not a streaming preparation workflow.

## Reviewing evidence and exclusions

The detached `molsysmt.covalent_inference@1` report contains sorted candidate
pairs and their methods, added pairs and resulting bond indices, a map from
original to resulting bond indices, source atom/structure/state indices, original
producer versions and the heavy/H/peptide exclusions. Candidate and added pair
arrays are `int64` with shape `(n_pairs, 2)`, including empty results.
`candidate_method_indices` is an aligned `int8` array indexing the three names
in `candidate_methods`; it avoids a string/list object per candidate. Peptide
distances and thresholds use typed PyUnitWizard QuantityRecords with explicit nm
units, independent of your session's output policy.

Local H-parent consensus can be applied while the complete group H-name inventory
remains unassessed. This choice is explicit in this policy and does not establish
protonation, terminal chemistry, missing H atoms or H placement. Unknown H names,
modified heavy-only H references, conflicting chemistry and unsupported groups
remain recorded; no alias or general distance fallback silently repairs them.
The local ACE/NME/NHE/NH2 references are available when those groups explicitly
declare `amber` or `legacy` naming. The shared heavy/H tools retain exact cap
layouts and the peptide tool admits only their permitted C/N backbone roles.
All ordinary conflict, geometry, chain and selection checks still apply. Unknown
cap conventions remain exclusions. This does not add a cap or infer a biological
terminus or complete terminal state. Read a PDB with `get_missing_bonds=False`,
declare its reviewed native naming context, then use this tool when cap support
is required. You can alternatively supply `from_naming_scheme` to public
conversion before the selected native reader engine executes. PDB reader
defaults do not assume a cap naming convention.
The report's `excluded_inference_policies` makes three fixed choices explicit:

| Scope | Policy |
| :--- | :--- |
| Disulfides | Retain stored edges; do not promote S-S proximity to a bond. |
| Metal coordination | Retain stored edges; infer no coordination from distance. |
| Groups without an exact template | Disable geometric fallback. |

`unsupported_group_indices` is an `int64` array of selected source group indices
without a template, including an empty `(0,)` result. It scopes the exclusion;
it is not an inventory of every unsupported group in an unselected system.
Waters, ions, arbitrary ligands and unreviewed modified groups remain unassessed.
The four curated MSE/SEP/TPO/MLY heavy references retain their own chemistry;
their sequence parents do not substitute for them.

You can separately call
{func}`molsysmt.interactions.disulfides.get_disulfide_candidates` with `pbc=False`
to inspect nonperiodic S-S proximity on the same structure. It returns geometric
candidates, including competing partners, without changing ChemicalStates.
Three nearby sulfurs can produce three candidates; this native inference policy
does not choose a matching or an oxidation state. Resolved PDB SSBOND/LINK/CONECT
edges remain stored even when contradictory, with the reader's conflict evidence.
An unresolved or unrepresented-symmetry declaration is not replaced by a nearby
base-cell pair. Retaining an edge does not recertify its chemistry. Review the
coverage and original declaration history before downstream preparation.

The group, H, peptide and application reports record `rule_version=2` for this
naming-scoped cap extension. Existing historical reports retain their original
rule version; the serializable dictionary schemas remain at version 1. The
additional policy fields document existing exclusions without changing which
pairs this method applies.

## Preserving historical provenance

Every successful operation, including no-addition results, archives the report
in the selected state's `ChemicalStates.get_preparation_history()`. Added rows
carry `provenance_index`, the index of that state's historical envelope. H5MSM
0.5 and ChemicalStatesDict preserve the record without coordinate snapshots.

Reports have `index_scope='operation'`: their indices and output dimensions
describe the original operation. Extraction/reordering retains the history,
remaps current bonds and preserves the history reference. Merging shifts current references
to these known local history records by the preceding inputs' history lengths,
while historical report axes remain unchanged. Other opaque provenance is not
reinterpreted. Later operations do not rewrite earlier reports into current axes.
Keep intervening maps and never
use a historical atom/bond index directly to address the current system.

New edges set connectivity completeness to `partial`; inference does not certify
a complete graph. Named interaction occurrences on the output become unevaluated
when bonds change, and the report names the affected analyses. A no-addition
operation retains them. Other chemical states and the reference-state selection
are preserved.

## Selecting the PDB reader engine

```python
prepared = msm.convert(
    pdb_file, to_form='molsysmt.MolSys',
    get_missing_bonds=True, bond_inference_engine='MolSysMT',
)
```

If the whole source uses one reviewed convention, include
`from_naming_scheme='amber'` (or another supported declaration) in that call.
The convention reaches classification and native inference before output
selection. A selection such as `group_type=='amino acid'` uses this interpreted
inventory. Mixed conventions need per-group native declarations instead of a
single file-wide claim. Reader history retains `source_naming_scheme`; later
metadata edits do not rewrite that historical input. The ordinary defaults and
structure-0 inference policy below remain unchanged.

File, text and `PDBFileHandler` routes support the same explicit engine choices
for native `MolSys` and `Topology` output:

| Request | Behavior |
| :--- | :--- |
| `get_missing_bonds=False`, engine omitted | Retain only resolved declared PDB edges; no inference engine runs. |
| `get_missing_bonds=True`, `bond_inference_engine='MolSysMT'` | Compose and apply this bounded native policy without importing OpenMM. |
| `get_missing_bonds=True`, `bond_inference_engine='OpenMM'` | Run the existing OpenMM PDB bond operation; provider absence or failure raises. |
| `get_missing_bonds=True`, engine omitted | Retain the legacy optional OpenMM policy; an unavailable/failed calculation warns and archives its cause before retaining only declared edges. |

An explicit engine together with `get_missing_bonds=False` is a conflicting
request and raises. Existing defaults remain form-specific: notably text-to-MolSys
defaults to disabled inference, so include `get_missing_bonds=True` when requesting
an engine there. No automatic native fallback is introduced.

Reader inference uses **source structure index 0**, before atom/structure
extraction, for one shared graph. Selectable per-structure inference belongs to
the standalone build tool. For ensembles whose connectivity changes, declare
chemical states and structure associations separately. PDB parsing remains eager.
The native reader continues using the default exact-name composition. To select
the alias composition, read explicitly without inference and call the standalone
build function with its named method; no reader flag silently changes that policy.

The reader archives `molsysmt.pdb_connectivity@1` outcomes, including disabled,
inferred, unavailable and failed operations, declaration-resolution flags,
producer versions and error type/message. The native route first records the
explicit parse, then archives `covalent_inference@1`. Resolved declared bonds
keep precedence over inferred evidence. Declaration diagnostics retain typed
per-record source locations, endpoint matches, alternate/symmetry scope and
conflicts, alongside their aggregate flags. Historical endpoints are not current
atom indices after extraction. Unsupported images and missing/ambiguous sites
remain explicit limitations; an accepted edge does not certify its chemical kind.
See {ref}`cookbook-pdb-connectivity-policy`.

:::{seealso}
:class: dropdown

- {ref}`cookbook-pdb-connectivity-policy`
- {ref}`Tutorial_Covalent_Bond_Candidates`
- {ref}`Tutorial_Peptide_Bond_Candidates`
- {ref}`Tutorial_Chemical_Templates`
:::
