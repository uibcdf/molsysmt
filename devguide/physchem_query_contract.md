# Tabulated property query contract

**Role:** normative for the implemented readers below. Fixes and guards are
owned by uibcdf/molsysmt#470 and uibcdf/molsysmt#471.

## Population and interpretation

| Reader | Supported element | Output |
| --- | --- | --- |
| `get_atomic_radius` (vdw / protor) | atom | Quantity in nm |
| `get_electronegativity` (pauling) | atom | Dimensionless quantity |
| `get_hydrophobicity` | group | NumPy array of dimensionless scores |
| `get_polarity` | group | List of dimensionless scores |
| `get_transmembrane_tendency` | group | List of dimensionless scores |
| `get_surface_area` | group | List of raw Collantes descriptors; unit review #473 |
| `get_area_buried` | group | NumPy array of existing Rose reference values |
| `get_buried_fraction` | group | List of existing Janin reference values |
| `get_volume` | fixed group axis, no element argument | NumPy array of existing Grantham reference values |
| `get_charge` (tabulated definitions) | group and documented higher aggregates | Existing elementary-charge wrapper; Collantes ECI semantics under review #475 |

The eight readers exposing a fixed element argument reject other elements with ArgumentChoiceError
before population lookup. An atom index is never substituted for a requested
group index. No aggregation is inferred for a definition without a documented
scientific meaning. Charge retains its existing definition/form-specific
aggregation rules; this repair does not redefine its OpenMM calculation.

## Selection and delivery

Public readers remain form-agnostic: required information is obtained through
basic.get and existing conversion/delivery routes. The requested syntax is
forwarded through every relevant query, including ProtOr classification and
its fallback radius lookup, group volume and buried-fraction queries.
`get_area_buried` has no syntax parameter: a caller may resolve alternate
syntax using public basic.select, then pass the resulting group indices.
Numeric lists keep their axis order/repetitions;
empty supported selections retain a length-zero result and their normal
container type. Alternative syntax requires its optional selection provider.
No selector translation or table algorithm belongs in the Viewer consumer.

Property values and containers are unchanged. The Collantes surface-area
unit/normalization is not certified: the raw-list contract remains explicit
pending the primary-reference review in uibcdf/molsysmt#473. No guessed
conversion is introduced. Other existing unit boundaries are preserved. This is selection/scope
repair, not a new scientific scale or a claim of complete preparation. Missing
non-placeholder group entries retain UnknownGroupInTableError; existing dummy
neutral handling is not broadened. Group labels do not establish a valid
chemical state. Tabulated charge scores are distinct from stored formal charges
and named partial-charge assignments. Existing scientific references remain
in owning tool documentation; this repair introduces no new attribution method.

## Guard

`tests/physchem/test_property_selection_contract.py` uses a declared three-group
fixture with different atom/group populations and literal reference values.
It checks MolSys and Topology, default/explicit/alternative syntax, numeric and
empty populations, repeated indices, native output types/units, unknown groups,
component charge aggregation and source nonmutation. Unsupported-level tests
must fail on element before interpreting an invalid selection. Native functions
are exercised without importing Viewer; addon reception remains separate.

## Collantes interpretation boundary

ISA and ECI are named side-chain QSAR descriptors in the original 1995 abstract
(PMID 7629809; DOI 10.1021/jm00014a022). The current ISA reader reproduces a
historical table, not a coordinate calculation or a new run of the original
method. Its raw list is neither a verified dimensional area nor a declaration
of dimensionlessness. Keep values and return types until the original formula,
table unit and normalization are checked under uibcdf/molsysmt#473. Related
ECI electric-charge units and aggregation require their own primary-reference
review in uibcdf/molsysmt#475. Existing wrappers and source parity are not
scientific validation of those interpretations.
