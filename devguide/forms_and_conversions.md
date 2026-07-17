# Forms and Conversions

This document defines the current adapter and conversion contract. Historical
adapter implementation notes are archived under `archive/assessments/`.

## Form adapter contract

Form adapters live under `molsysmt/form/`. Each adapter module defines:

- `form_name`;
- `form_type`;
- `form_info`;
- `attributes` and `has_attribute`;
- applicable topological, structural, or general piping targets;
- `_convert_to`, mapping supported target form names to converter callables or
  lazy converter-module names.

Detailed file layout and dependency rules are defined in
`form_adapter_implementation.md`.

## Discovery and dependencies

Adapters are discovered lazily. Optional dependency ownership is defined by
`molsysmt/_depdigest.py`; adapters must not introduce their own competing
dependency registry. Soft dependencies are imported inside guarded functions,
never unconditionally at module import time.

## Conversion resolution

The current one-to-one resolver in `molsysmt/basic/convert.py` supports:

1. a direct edge from the source adapter to the target adapter; or
2. a two-edge route through `molsysmt.MolSys` when both edges exist.

It does **not** perform a general shortest-path search over the conversion graph.
Multiple-input conversions use registered shortcuts and attribute-based assembly
logic, with a MolSys route where explicitly supported.

Do not document or rely on arbitrary multi-hop conversion. A broader graph
resolver would be a new architectural feature requiring deterministic routing,
lossiness and cost policies, cycle detection, dependency-aware edge selection,
and dedicated tests.

## Converter registration

Register a converter only when it is callable for the documented source and
target contract. A placeholder that raises `NotImplementedMethodError` must not
be present in `_convert_to`, because registration advertises an executable edge.

Converter values may be callables or strings naming the converter module and
function. String entries preserve lazy imports; `_convert_one_to_one` imports the
module only when that edge is traversed.

Converters must:

- preserve documented semantics or explicitly document intrinsic loss;
- normalize native element IDs to strings;
- preserve coordinate, box, and time units through PyUnitWizard boundaries;
- accept the standard selection and structure-index arguments that apply to the
  represented data;
- import optional libraries lazily under DepDigest control.

MolSysMT canonical lengths are in nm and time is in ps. Angles derived from box
geometry follow the API's radians convention; converters must not generally
standardize angular data to degrees.

## Attribute declarations and piping

`attributes.py` records the adapter capability contract used by dispatch. A
declared attribute must be deliverable through the public `get()` path for every
documented element scope. Delivery may be direct or may use the adapter's
declared piping target.

This is intentionally a public-delivery definition, not merely a statement that
the source object's Python class stores a field directly. If native presence must
be distinguished from converted delivery in the future, add explicit metadata;
do not overload one boolean with two contradictory meanings.

For attributes available from more than one element scope, every corresponding
getter must exist or the pipe target must provide it. For example, coordinates
declared for both atoms and the system must work for both explicit atom requests
and the default system request.

Known delivery gaps are tracked under `pending_bugs/` and take precedence over
historical claims of complete adapter verification.

## Forms with partial source information

A source containing coordinates but no topology must not invent semantic
topology. Likewise, a topology-only form must not advertise structures. Where a
format contains only partial labels, a converter may construct only the topology
that can be justified from those labels and must document the inferred fields.

File handlers should accept the documented path-like representation at public
boundaries. Internal reader objects must not be assumed to retain a recoverable
filename after construction unless their actual API guarantees it.

### Contractual reduced trajectory forms

Tier 1 trajectory forms can have a deliberately structural contract. In
particular, DCD and XTC do not supply a molecular topology. Standalone
conversion may create an index-only native topology so that structural arrays
remain usable, but it must leave semantic atom IDs and chemical attributes
missing rather than fabricate them.

The contractual read scope is:

- `file:gro` and `molsysmt.GROFileHandler`: atom and group labels present in the
  file, coordinates, optional velocities, and orthogonal or triclinic box;
- `file:dcd` and `mdtraj.DCDTrajectoryFile`: coordinate frames, optional box,
  frame selection, atom selection, and source-frame indices as structure IDs;
- `file:xtc` and `mdtraj.XTCTrajectoryFile`: coordinates, box, time, frame
  selection, atom selection, and the stored XTC step as structure ID.
- `file:h5` and `mdtraj.HDF5TrajectoryFile`: embedded MDTraj topology,
  coordinates, optional velocities, box, time, temperature, and available
  kinetic and potential energies. This interoperability format is distinct
  from MolSysMT's native H5MSM persistence contract.

MDTraj reader adapters preserve the caller's file cursor during public getters
and native conversion. DCD coordinates cross the MDTraj boundary in angstroms;
XTC coordinates cross it in nanometers. Both are normalized through
PyUnitWizard and delivered in MolSysMT's canonical units.

This reduced contract does not claim that conversion back to an open reader
object can materialize arbitrary subsets without creating a new file. Writing,
append behavior, and reader-object subset materialization require separate
conversion edges and tests before they become contractual.

### Contractual MDAnalysis forms

`MDAnalysis.Universe`, `MDAnalysis.AtomGroup`, and `MDAnalysis.Topology` are
Tier 1 interoperability forms within an explicit, target-aware scope:

- `MDAnalysis.Topology` represents topology only. Atom subsets are
  materialized without structures; a structure request is rejected.
- `MDAnalysis.Universe` delivers its available topology together with
  coordinates, optional velocities, time, and orthogonal or triclinic box
  geometry. Random frame access and conversion restore the caller's active
  frame.
- `MDAnalysis.AtomGroup` is treated as a real subset. Converting or extracting
  it must not silently reintroduce atoms from its parent Universe, and further
  atom selections are relative to the AtomGroup.
- Native `atom_id`, `group_id`, and `chain_id` values retain source identity as
  strings; duplicate source IDs are not renumbered merely to make them unique.
- MDAnalysis residues and segments map to MolSysMT groups and chains. Components,
  molecules, and entities are rebuilt from the information available after
  import; they are not claimed to be native MDAnalysis hierarchy levels.
- Available covalent bonds and formal charges enter the native chemical-state
  seam. Opaque MDAnalysis bond-type objects are reported as an adapter
  limitation rather than guessed into a canonical chemical type.

Self-conversion to a Universe or AtomGroup materializes the requested atom and
frame subset in memory. MDAnalysis's `MemoryReader` represents a uniform time
axis; a selected irregular time axis is therefore rejected with an actionable
error instead of being silently regularized. Conversion to `molsysmt.MolSys`
retains irregular time arrays.

This contract does not promise preservation of arbitrary user-added MDAnalysis
topology attributes, transformations, auxiliary readers, analysis caches, or
custom trajectory-reader state. Those features require separate evidence before
they can be advertised as contractual.

### Contractual chemical interoperability forms

`rdkit.Mol`, `openff.Molecule`, `openff.Topology`, `parmed.Structure`,
`string:smiles`, `file:smi`, `file:mol2`, and `file:psf` are Tier 1 within target-aware
chemical contracts:

- RDKit preserves supported native graph fields, atom and bond stereo,
  aromaticity, isotope, formal charge, conformers, namespaced identity, and
  complete supported partial-charge properties.
- OpenFF Molecule preserves conformers, complete partial charges, rich atom and
  bond chemistry, and E/Z reference atoms. OpenFF Topology combines molecule
  graphs and complete charges but does not invent a synchronized trajectory
  from independent per-molecule conformers.
- ParmEd Structure preserves coordinate frames, unit cells, B factors, source
  atom types, chemical bond fields, formal charge, and mechanical partial
  charge. Per-atom mechanics follow atom extraction.
- SMILES strings and SMI files are reduced graph forms without partial charges
  or structures. Invalid SMI records fail with their source line, and multiple
  records become disconnected components in one requested `rdkit.Mol` target.
- MOL2 uses ParmEd as an encapsulated parser while MolSysMT validates Tripos
  source tokens. It preserves serials, names, Tripos atom types, groups,
  coordinates, optional box, partial charges, bond IDs, aromatic `ar`, and
  fractional amide `am` order. Unsupported bond tokens and multi-record files
  fail explicitly.
- PSF uses OpenMM as its parser and preserves source string IDs, chemical atom
  types inferred by the parser, CHARMM force-field atom types, partial charges,
  hierarchy, and complete explicit covalent connectivity. Ordinary PSF
  connectivity does not encode chemical bond order, so no order is invented.
  PSF itself has no structures; coordinates supplied separately are composition
  input rather than attributes read from the file.

These contracts do not imply arbitrary property-block preservation or a
multi-record SDF/MOL2 model. Those require a separate post-1.0 schema decision.

## Validation obligations

For every supported conversion edge, tests should cover:

- direct execution through `msm.convert`;
- representative selection and structure slicing;
- ID, shape, dtype, and unit invariants;
- lossless round-trip parity where the formats can represent equivalent data;
- explicit expectations for intentionally lossy formats;
- missing optional dependency behavior;
- lazy-import behavior for soft dependencies.

The adapter linter checks structural conformance. It is not evidence of semantic
parity or scientific correctness.
