---
summary: Add SDF file form with MolSys conversion
issue: uibcdf/molsysmt#215
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Add SDF file form with MolSys conversion

**Reported:** 2026-09-22, from the DockingMT ligand-interchange discussion and inspection of the form registry.
**Status:** Open proposal; no SDF file form is implemented in MolSysMT.

## What

Add a file:sdf form with supported conversions in both directions with
molsysmt.MolSys, initially for one molecular record. This establishes an
ordinary MolSysMT file form for ligand exchange. The broader SDF metadata and
multi-record design already appears in
[chemical_metadata_preservation_sdf_mol2.md](chemical_metadata_preservation_sdf_mol2.md);
this proposal makes the smaller conversion deliverable explicit. Track the
DockingMT consumer in uibcdf/dockingmt#3.

## How

- Register file:sdf in the form catalog with working public conversion routes
  to and from MolSys. Reuse an existing optional chemical toolkit internally
  where appropriate, without exposing its object as the result or importing it
  eagerly.
- Define one-record semantics for molecular graph, atom and bond identity,
  bond order and aromaticity, formal charge, stereochemistry, and coordinates
  where the selected SDF variant represents them. Convert angstroms to
  MolSysMT nanometers and keep native element IDs as strings. Declare only
  attributes actually delivered by public getter or conversion routes.
- State how one MolSys structure is chosen for output. Multiple structures
  and multiple SDF records require an explicit, tested policy; until a
  multi-record model is accepted, reject unsupported cases rather than silently
  taking the first record or frame.
- Detect SDF property blocks that MolSys cannot represent yet. Report their
  loss clearly, including under strict conversion, rather than treating a
  parsed graph as a complete round trip. The separate metadata proposal retains
  ownership of a durable property-block and multi-molecule schema.

## Why

SDF is a common ligand interchange format, and MolSysMT's existing purpose
includes converting file forms to its native molecular-system representation.
The current form catalog has RDKit molecular forms and MOL2 files, but no
file:sdf form. One shared conversion path lets DockingMT use the same MolSys
input model for ligand data without owning general SDF parsing. This is an
architectural judgement, not a measured performance claim.

## What is measured and what is assumed

**Inspected:** molsysmt/form has no SDF adapter.
[forms_and_conversions.md](../forms_and_conversions.md) explicitly leaves
property blocks and a multi-record SDF/MOL2 model to a separate schema
decision. No round-trip fidelity or performance measurement was made.

**Assumed:** Single-record conversion is useful before the broader metadata
and multi-record model is settled. Representative fixtures must establish
which SDF features the first adapter supports faithfully.

## What was refuted

Treating rdkit.Mol support as equivalent to file:sdf support leaves no
discoverable file form or direct MolSys file conversion contract. Claiming
unqualified SDF round-trip fidelity would hide property-block and record
boundary loss.

## Scope and exclusions

This issue covers the first file:sdf form and single-record conversions.
Arbitrary property-block preservation, multi-molecule files, and a general
record-to-MolSys schema remain in the existing broader proposal. DockingMT's
ligand preparation and Vina protocol are outside this adapter. A string:sdf
form may be proposed separately if a consumer needs it.

## Acceptance criteria

- The public form catalog recognizes .sdf files, and conversion works between
  file:sdf and MolSys in both directions for documented one-record inputs.
- Representative fixtures preserve supported graph, chemical attributes,
  coordinates, units, and atom alignment through a MolSys round trip within
  the format's precision. Tests cover selection and structure-index semantics
  where meaningful.
- Multiple records, multiple frames, and unsupported properties receive
  explicit, tested behavior. No record or property is silently dropped while
  reports or strict mode claim exhaustive preservation.
- Capability declarations, instance-aware presence, optional dependency
  behavior, docstrings, User Guide, Cookbook, and applicable course material
  match the delivered subset.
- The durable contract is incorporated into
  [forms_and_conversions.md](../forms_and_conversions.md) before closure.

## Dependencies and risks

Stereochemistry and aromaticity can change under parser normalization rules;
fixtures and fidelity claims must distinguish source information from inferred
chemistry. The deferred metadata proposal remains the owner of any broader
SDF property and multi-record schema.
