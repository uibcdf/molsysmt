# Native query contract

**Role:** normative implementation and public-contract guidance.
**Tracking:** uibcdf/molsysmt#128; boundary repair uibcdf/molsysmt#391;
nullable selected counts uibcdf/molsysmt#392.

## Public entry points

Resident `MolSys`, `Topology`, `Structures`, `ChemicalStates`, `Interactions`
and `MolSysBuilder` inherit `get()` and `info()` from
`molsysmt/native/queries.py`. These methods use the basic-tool attribute
catalogue, argument semantics, quantity policy and output assembly.

The receiver supplies the free functions' `molecular_system` argument. Preserve
the existing MolSys/Builder positional order:

```python
get(element='system', selection='all', structure_indices='all', mask=None,
    syntax='MolSysMT', get_missing_bonds=True, output_type='values',
    skip_digestion=False, *, chemical_state='reference', **kwargs)

info(element='system', selection='all', syntax='MolSysMT', skip_digestion=False,
     *, mask=None, structure_indices='all', output_type='styler')
```

Using named options gives the same experience as `basic.get`/`basic.info`.
Unlike the free functions, `chemical_state` in native `get` and
`structure_indices`/`output_type` in native `info` are keyword-only. Do not
reinterpret old positional syntax/skip arguments as structure/output options.

`get` delivers one value, an ordered list of values or a requested attribute
dictionary. `info` delivers a Styler by default, a DataFrame or dictionary
records. Unsupported/absent attributes follow the basic query contract; no
additional hierarchy or chemical assignment is invented. A partial MolSys
does not require topology for a system summary.

## Validation ownership

Each native public method has an ArgDigest boundary and SMonitor signal. The
native decorator's local registry reuses existing value digesters with their
basic query semantic context. It does not copy their rules or weaken their
attribute-flag validation. Alias tables reuse `get_argument_aliases()` and
keyword admission reuses the canonical attribute domain.

Native wildcard registrations belong only to those methods' decorator plans;
they do not broaden other APIs' aliases or keyword domains. Inherited native
methods retain their contract under a subclass's runtime caller. Constructor
validation remains a separate existing contract.

Private execution/provider helpers are undecorated. Trusted provider calls
receive normalized options, selected indices validated against the available
axis and catalogued attribute flags. `skip_digestion=True` remains reserved for
values already satisfying that complete callee contract. No value-passport or
permanently validated mutable-object state is introduced.

## Shared execution

`basic.get._get` and `basic.info._info` contain shared internal execution and
table assembly. The general public functions supply universal discovery,
complementary-form search and conversion pipes. Native methods supply a known
single-domain provider instead:

- Resolve the adapter for the known native class without `get_form`.
- Use that adapter's existing attribute availability and specific getters;
  avoid general `where_is_attribute` searches and conversion pipes.
- Validate explicit axes with the shared index validators and native counts.
- Reuse attribute grouping, derivations, ID/scalar normalization and quantity
  standardization from the common executor.
- Share `info` columns and presentation, including evaluated structure scope.

Output assembly returns exact built-in scalars directly when the attribute is
outside the canonical physical-unit wrapping table. Such values cannot be
quantity-backend objects. Physical fields retain wrapping/standardization, and
custom numeric subclasses and array/quantity containers retain the ordinary
quantity inspection path. This avoids emitting quantity-probe misses for plain
counts without changing the unit policy or weakening a public boundary.

Native methods do not call the decorated universal `get`/`info`. Specific form
providers remain reused; this is not a rewrite of every attribute getter or
native table. There is no persistent cache of mutable values/counts and no
whole-system copy/build just to locate an attribute. Explicit indices retain
order/repetitions; mask intersections retain existing sorted-unique semantics.

## Supported domains

| Object | Current molecular query scope |
| --- | --- |
| MolSys | Its supported topology, chemical-state, structure and mechanics attributes; available partial domains and declared axes. |
| Topology | Supported inventory/hierarchy/connectivity and state-dependent attributes through its existing chemical-state facade. |
| Structures | Supported structural attributes and axis counts. Specialized `get_coordinates`, `get_box`, `get_time` and other existing getters remain available. |
| ChemicalStates | Current adapter metadata: atom count, state count and reference-state index. Specialized bonds/history access remains available; a new atom-assignment query schema is not implied. |
| Interactions | Current adapter metadata: declared atom and structure domains. `query`, `between_selections` and `to_page` remain the occurrence/coverage/measurement API. |
| MolSysBuilder | Its declared editable domains; no `build()` or finalization is required. |

Chemical-state resolution retains existing supported cases and refusal rules.
In particular, explicit non-reference state resolution currently requires the
existing native Topology/MolSys path, and structure-associated state selection
requires a MolSys with unambiguous associations. Giving ChemicalStates a
metadata `get` does not silently extend that resolver.

## Selection boundaries

All/unrestricted and flat explicit index queries use the native provider's
direct selection path. Boolean masks use shared mask validation; numeric
intersections preserve existing selection semantics. Expression languages,
nested selections and expression masks retain `basic.select` and its existing
parser/providers. These cases are supported fallbacks, not claimed to eliminate
universal dispatch throughout an expression evaluation.

The requested structure scope is passed to every summary acquisition and
recursive expression-mask selection. Selected hierarchy counts exclude missing
parents and deduplicate only declared memberships; full-system counts retain
the complete declared inventories. Typed counts retain their existing group
or molecule type definitions. No missing group is labelled a small molecule.

Standalone Structures atom counts use native observable alignment, including
velocity/B-factor/occupancy-only payloads. Time/box-only containers have the
existing native zero atom count; time does not infer atoms. MolSys retains its
separate partial-domain rules for an undeclared atom axis. Shape-only `repr`
remains distinct from this validating data query.

## Declarative dictionary queries

`TopologyDict` and `MolSysDict` continue to use `msm.get()` and `msm.info()`;
they do not acquire the resident instance methods. Their topological adapters
read these values without copying or finalizing a native object:

- `n_atoms` from the system or an atom selection;
- `atom_index` from atoms;
- `atom_id`, `atom_name` and `atom_type` from atoms when the requested fields
  are already stored strings.

Flat atom selections preserve order/repetitions and basic-tool index/mask
validation. Lists returned for stored labels are detached. There is no cache:
later dictionary edits are observed. These queries read the requested inventory;
they do not validate unrelated hierarchy, chemistry or coordinate payloads.

Missing or non-string atom fields retain the converter's normalization,
defaults and element inference. Nested selections retain the existing native
route. Other topological getters and complete `info` summaries still use the
declared conversion pipes. In particular, group, chain, molecule and entity
counts cannot generally be replaced by serialized list lengths: finalization
can supply missing memberships or infer parents.

The private form probe `_can_get_without_conversion` allows the shared basic
executor to bypass a bulk pipe only when every requested field has a direct
route for the actual selected indices. Unsupported/mixed queries keep ordinary
piping, including complementary forms. Do not set the general pipe metadata to
`None` merely because a subset of getters becomes direct.

These are reads of the existing 0.1 schema, not a new dictionary format or a
multi-state chemical serialization contract. Existing structure/unit delivery
and non-reference chemical-state restrictions remain unchanged.

## Evidence and remaining scope

The semantic and mechanism guards live in
`tests/native/test_native_queries.py`. They assert independently expected
counts, hierarchy links, coordinates, units and errors, and prohibit universal
discovery/conversion for claimed direct cases. Existing basic/native/interaction
tests protect general delivery and sparse result behavior.

The dated performance study and reproducer are maintained in
[the #128 record](pending_proposals/native_query_shortcuts.md) and
`benchmarks/native_queries.py`. Compare fully validated routes; narrower
property/trusted-adapter costs are not equivalent native-query speedups.

Dictionary forms, file handlers, ViewerJSON, Simulation and experimental
MolecularMechanics do not acquire these instance methods. Direct dictionary
reads beyond the bounded atom inventory and specialized disk access remain
pending study scope. Stored-atom query and fallback guards live in
`tests/form/molsysmt_TopologyDict/test_direct_queries.py` for both dictionary forms.
No new dependency, numerical method, Rust kernel or persistence format is added.
