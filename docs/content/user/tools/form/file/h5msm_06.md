(user-tools-form-h5msm-06)=
# H5MSM 0.6 (experimental)

*Preserving stored mechanical parameters and their original evidence.*

H5MSM 0.6 adds an optional `molecular_mechanics` layer to the independently
owned domains of {ref}`H5MSM 0.5 <user-tools-form-h5msm-05>`. Request it explicitly
with `format_version="0.6"`; ordinary writing still uses 0.5. The development
schema and its public routes are experimental. The intended first stable format
is H5MSM 1.0 after whole-format and consumer qualification.

## Writing and recovering a system

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import molsysmt as msm
from molsysmt.native import MolSys, Structures

molsys = MolSys(n_atoms=2)
molsys.structures = Structures(
    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
)
molsys.molecular_mechanics.forcefield = "unresolved_model_request"
molsys.molecular_mechanics.partial_charge = [0.25, -0.25]
molsys.molecular_mechanics.cutoff_distance = msm.pyunitwizard.quantity(12, "angstrom")

with TemporaryDirectory() as directory:
    path = Path(directory) / "prepared.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=path,
                format_version="0.6")
    molsys_A = msm.h5msm.read(path)
    assert molsys_A.molecular_mechanics.forcefield == "unresolved_model_request"
    assert msm.get(path, forcefield=True) == "unresolved_model_request"
    assert msm.h5msm.read_axis_sizes(path)[("molecular_mechanics", None, "atom")] == 2
```

`msm.h5msm.write(molsys, path, format_version="0.6")` uses the same codec.
Reading restores stored values and reports; it does not resolve a force field,
recalculate charges/types, register attribution, or rebind scientific evidence.
A model name is a request, not proof of a completed parameterization. Original
scientific producer versions remain distinct from the file writer's version.
Existing stale or unknown assignments remain stale or unknown. Reports with
unknown/incomplete scientific schemas can be stored and copied as evidence,
but scientific PDBQT export and atom projection refuse them with
`StructuralInconsistencyError`; storage does not make them usable assignments.

New 0.6 writes stage a private file beside the destination, close it successfully,
and publish it atomically without replacing an existing path. This requires
hard-link support. Normal failure removes staging; abrupt process termination
may leave a private staging file. Atomic visibility is not crash durability.
Ordinary byte copying retains the separate `msm.copy` destination contract.

## Inspecting independent domains

`msm.h5msm.read_layers(path, layers="molecular_mechanics")` returns the stored
native object without loading the other domains. Use
{func}`molsysmt.h5msm.read_axis_sizes` for its declared atom count, including
parameter-only layers without atom rows. Endpoint keys are
`(layer, analysis_name, axis)`; `analysis_name` is None except for interactions.
Axes are `atom`, `structure` and chemical `state`. Absent or unknown axes are
omitted. This reads declared metadata, not complete payload validation.

A standalone mechanical layer requires `mechanics_n_atoms`:

```python
from molsysmt.native import MolecularMechanics

with TemporaryDirectory() as directory:
    path = Path(directory) / "mechanics.h5msm"
    msm.h5msm.write_layers(
        path, molecular_mechanics=MolecularMechanics(forcefield="request"),
        mechanics_n_atoms=7, format_version="0.6",
    )
    assert msm.get(path, n_atoms=True) == 7
    mechanics = msm.convert(path, to_form="molsysmt.MolecularMechanics")
    assert mechanics.forcefield == "request"
```

Independent layers can have different atom populations and explicit maps.
Resident `MolSys` assembly requires connected, declared identity maps for shared
atom and structure axes; matching counts alone are insufficient. Nonidentity
maps remain available through independent reads. `MolSys` cannot represent a
mechanics-only file, or the distinct presence of an entirely empty mechanical
layer or named-analysis collection; resident assembly refuses those cases.
Present-empty mechanical reports/tables have native markers and remain supported.
A complete independent mechanics projection reads only that layer when requested
with all axes and default conversion context, without strict/report or extra
options. It does not validate unrequested layers or declare their association.

`molsysmt.H5MSMFileHandler` remains a 0.3/0.4 handler and refuses 0.5/0.6.
Use resident conversion, selected-layer reads, queries or structural iteration.

## Querying and modifying represented data

Public `get`, `select` and `has_attribute` support modular paths. Selected
coordinate queries and structural iterators retain their bounded row/atom reads;
unrequested mechanics stays unloaded. Mechanical queries decode the mechanical
domain once per query scope, including its stored reports/table. They do not
load coordinates, topology or chemical states. Static-domain reads are resident,
not constant-memory column queries.

Partial-charge getters return canonical elementary-charge magnitudes as they do
for native objects. Mechanical scalar quantities retain their explicit stored
units. Public `formal_charge` queries read authoritative ChemicalStates, even
when a legacy formal-charge column is also stored in mechanics.

`msm.copy(path)` preserves file bytes. `msm.extract(path, ..., output_filename=...)`
preserves a 0.6 source's version while using native atom/state/analysis remapping.
Native atom selection uses ascending unique source indices; structure selection
retains order and repetitions. Subset conversion can load complete source domains.
Use `msm.convert(..., format_version="0.6")` for explicit file conversion; its
default remains 0.5 and refuses stored mechanics rather than dropping it.

Complementary partial `MolSys` objects/files can supply one stored mechanical
domain with matching atom rows, including reports without parameters. Repeated
nonempty mechanical providers refuse; their reports are not merged or replaced.
Supplying the list declares positional correspondence. It does not authenticate
system identity.

`msm.h5msm.append_structures` supports topology-free 0.6 files without interactions,
including a compatible mechanical layer and an explicit Structures-to-ChemicalStates
map. Existing mechanical values/evidence remain stored evidence. State indices are
required when extending an existing state map. Validation precedes resizing;
append is not crash transactional. Unsupported compositions refuse. For other
modifications, load a resident system, use its supported editing tools and write
a new file; the legacy handler is not a modular mutation interface.

## Experimental storage contract

Root metadata is explicit text: `type="h5msm"`, `version="0.6"`, `creator`,
`creator_version` and UTC `created_at`. The existing topology, chemical-state,
structural and sparse-analysis layer schemas are reused. New mechanics uses:

```text
molecular_mechanics/             attributes: schema_version=1, n_atoms
    snapshot/                   attribute: schema_version=1
        json                    uint8 UTF-8 tagged metadata tree
        arrays/0, arrays/1, ...  typed numeric/boolean/fixed-width UTF-8 datasets
```

The tree contains exactly `settings`, `atoms_ff`, `partial_charge_assignment`
and `atom_type_assignment`. The sixteen scalar settings include text model
requests; explicit boolean settings; finite dimensionless dielectric/tolerance
values; length (`cutoff_distance`, `switch_distance`), mass (`hydrogen_mass`),
concentration (`salt_concentration`) and inverse-length (`kappa`) quantities.
Dimensional settings use sealed PyUnitWizard records with explicit field and
dimension validation, retaining compatible original units without changing the
reader's unit policy. Scalar quantity magnitudes decode as zero-dimensional
arrays with their stored numeric dtype.

An optional zero-based atom table stores ordered `partial_charge`, legacy
`formal_charge` and `atom_ff_type` columns. Charges have a fixed elementary-charge
protocol. The legacy mechanical formal-charge column does not replace chemical
assignments. Supported numeric/object, nullable integer/float and Python-backed
string dtypes retain their null semantics. Present-empty tables/reports differ
from absence. Structural textual IDs retain the existing object-array read
representation; their labels are unchanged.

Reports retain original producer, attribution, historical maps and detached
assignment evidence. Typed primitive/mapping/list/tuple/array nodes preserve
values without expanding bulk arrays into Python records or JSON/Base64 lists.
Unsupported objects, extensions, cycles, fields, units, versions and malformed
references refuse. This is a snapshot of the bounded native domain, not an
external engine checkpoint, an arbitrary object serializer, or a complete
Hamiltonian representation. Independent scientific and installed-client
qualification remain required before the stable-format freeze.
