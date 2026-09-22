---
summary: Add PDBQT file and string forms with MolSys conversion
issue: uibcdf/molsysmt#214
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

# Add PDBQT file and string forms with MolSys conversion

**Reported:** 2026-09-22, from the DockingMT Vina integration discussion and inspection of the form registry.
**Status:** Open proposal; no PDBQT form is implemented in MolSysMT.

## What

Add file:pdbqt and string:pdbqt forms with supported conversions in both
directions with molsysmt.MolSys. These are general molecular-system forms in
MolSysMT, even when a docking program is the first consumer. Track the
downstream use in uibcdf/dockingmt#3.

## How

- Register both forms through the normal lazy form catalog and dependency
  mapping. Provide working public conversion routes to and from MolSys; a
  file/string bridge may share one parser and writer internally.
- Define the first supported layouts: a rigid receptor and a single ligand
  with a valid torsion tree. Unsupported flexible-receptor and multi-model
  variants must fail explicitly until their semantics are specified.
- Map only fields PDBQT carries: coordinates, atom identity, partial charge,
  AutoDock atom type, and available torsion information. Convert angstroms to
  MolSysMT nanometers and keep native element IDs as strings. Do not infer
  complete connectivity or bond orders from absent PDBQT data.
- Require writer inputs appropriate to the selected layout, including atom
  typing, charges, geometry, and ligand torsion data. Missing or inconsistent
  input must fail clearly; serialization must not silently perform chemical
  preparation. Use conversion reports and strict mode for representational loss.
- Declare attributes only where public getters actually deliver them, with
  instance-aware presence. Any parser/writer backend remains optional and
  lazy. This proposal does not require Meeko.

## Why

DockingMT's current Vina adapter supplies a receptor PDBQT file and a ligand
PDBQT file or string to Vina. A shared PDBQT form lets DockingMT use MolSysMT's
native molecular-system representation without embedding general file parsing
and writing in its docking layer. This is an architectural judgement based on
source inspection, not a performance claim.

## What is measured and what is assumed

**Inspected:** molsysmt/form has no PDBQT form. Existing file and string forms
use registered conversion edges and capability declarations. DockingMT's
dockingmt/engines/vina.py supplies PDBQT inputs to Vina. No timing or
chemical-fidelity measurement was made.

**Assumed:** A useful first subset can be specified without treating every
PDBQT dialect as equivalent. The exact dialect fixtures need to be chosen
during implementation.

## What was refuted

Keeping PDBQT only inside DockingMT leaves a general file form unavailable to
other MolSysMT consumers. Converting directly into Vina's private engine state
does not provide a public file or string form contract.

## Scope and exclusions

This issue owns PDBQT recognition, parsing, writing, capability metadata,
conversion semantics, and fidelity tests. It does not own general charge
assignment, hydrogen placement, atom typing, or rotatable-bond perception;
those are separate preparation capabilities to specify later. It does not
own DockingMT protocol decisions or Vina execution.

## Acceptance criteria

- Form discovery recognizes PDBQT files and explicit PDBQT strings; public
  conversion works in both directions between each form and MolSys.
- Representative rigid-receptor and flexible single-ligand fixtures parse and
  serialize with correct atom alignment, coordinates, units, supported charges,
  types, and torsion records. Tests compare equivalent supported content
  across file, string, and MolSys routes.
- Missing writer inputs and unsupported layouts fail with actionable errors.
  Lost attributes are not claimed as preserved by capability declarations or
  reports; strict mode rejects known loss.
- Tests cover selection and structure-index behavior where meaningful,
  optional dependency behavior, and public API routes. Docstrings, User Guide,
  Cookbook, and applicable course material describe the supported subset.
- The durable contract is incorporated into
  [forms_and_conversions.md](../forms_and_conversions.md) before closure.

## Dependencies and risks

The ligand writer needs a specified torsion-tree input contract. If MolSys
cannot carry it, resolve that general representation separately before
claiming flexible-ligand output. PDBQT atom types are not necessarily general
force-field atom types; their mapping must be explicit. The downstream
consumer is tracked in uibcdf/dockingmt#3.
