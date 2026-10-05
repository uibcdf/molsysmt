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
Disulfides, metals, terminal caps and arbitrary small-molecule connectivity
require separate policies. Review those limitations before downstream preparation.

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

The reader archives `molsysmt.pdb_connectivity@1` outcomes, including disabled,
inferred, unavailable and failed operations, declaration-resolution flags,
producer versions and error type/message. The native route first records the
explicit parse, then archives `covalent_inference@1`. Resolved declared bonds
keep precedence over inferred evidence. Current declaration flags are aggregate
evidence; they do not provide a complete per-record malformed-file diagnosis.

:::{seealso}
:class: dropdown

- {ref}`cookbook-pdb-connectivity-policy`
- {ref}`Tutorial_Covalent_Bond_Candidates`
- {ref}`Tutorial_Peptide_Bond_Candidates`
- {ref}`Tutorial_Chemical_Templates`
:::
