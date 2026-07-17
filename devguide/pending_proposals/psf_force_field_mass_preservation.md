# Preserving PSF Force-Field Atom Masses

**Status:** post-1.0 schema proposal

## Why

The CHARMM PSF `NATOM` table stores a mass for every atom. This value can be a
force-field parameter and is not necessarily identical to the physicochemical
mass inferred from the element or isotope. The Tier 1 PSF reader preserves the
source force-field atom type and partial charge, but the current native
`MolecularMechanics.atoms_ff` table has no field for a per-atom force-field
mass. Mapping the source value to the ordinary derived `mass` attribute would
silently merge two distinct authorities.

## Proposed model

Consider adding an optional `atom_ff_mass` column to
`MolecularMechanics.atoms_ff`, with atomic-mass units and the same positional
alignment contract as `partial_charge` and `atom_ff_type`. Absence must remain
cheap: forms without explicit parametrized masses should not allocate the
column.

## How

1. Audit OpenMM, ParmEd, Amber topology, GROMACS topology, and H5MSM semantics
   to distinguish source force-field masses from element/isotope masses.
2. Define precedence and provenance when both a physicochemical mass and a
   parametrized force-field mass are available.
3. Add `atom_ff_mass` to the central attribute policy, native mechanics object,
   dictionaries, H5MSM schema, extraction, merge, and comparison behavior.
4. Import PSF `NATOM` masses with explicit units and test atom-subset alignment.
5. Export the value only to targets whose model distinguishes or explicitly
   accepts force-field masses; otherwise report the intentional loss.
6. Update the User Guide, API docstrings, and course material before exposing
   the attribute publicly.

## Acceptance criteria

- No source force-field mass is presented as an element-derived mass.
- Missing `atom_ff_mass` data does not allocate a full null column.
- Atom extraction, merge, serialization, and round trips preserve alignment,
  dtype, units, and provenance.
- Conversion reports identify targets that cannot represent the value.
