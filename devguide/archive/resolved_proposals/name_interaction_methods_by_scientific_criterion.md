---
summary: Name interaction methods by scientific criterion
issue: uibcdf/molsysmt#276
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [api, docs]
guard: tests/interactions/test_scientific_attribution.py
normative:
blocked_by: []
supersedes: []
---

# Naming interaction methods by scientific criterion

**Reported:** 2026-10-01, maintainer request during the interaction attribution review.
**Status:** Implemented with compatibility aliases and validated observations.

## What

Separate the mathematical criterion from the exact chemical/geometry profile
and its reference implementation. Preserve historical software selectors as
compatibility aliases without attributing discovery to the software.

## How

`molsysmt/_private/interaction_methods.py` owns resolution. Existing numerical
dispatch labels remain private and numerical criteria do not change. The public
`profile` argument is keyword-only. Results retain canonical method/profile,
a versioned definition identifier, effective parameters and pinned references.
Existing files retain their original metadata when read.

| Family | Canonical method | Profile | Compatibility selector |
| --- | --- | --- | --- |
| Hydrogen bonds | `baker_hubbard` | `nitrogen_oxygen` | unchanged |
| Hydrogen bonds | `wernet_nilsson` | `nitrogen_oxygen` | unchanged |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `elemental_fon` | `cpptraj` |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `smarts_donor_acceptor` | `prolif` |
| Hydrogen bonds | `donor_acceptor_distance_angle` | `explicit_sites` | `mdanalysis_geometry` |
| Cation-pi | `centroid_distance_angle` | `smarts_5_6` | `prolif` |
| Cation-pi | `centroid_distance_offset` | `three_atom_plane` | `molstar_geometry` |
| Cation-pi | `centroid_angle_offset` | `least_squares` | unchanged |
| Pi-pi | `plane_angle_intersection` | `smarts_5_6` | `prolif` |
| Pi-pi | `plane_angle_intersection` | `aromatic_cycles` | `mdtraj_geometry` |
| Pi-pi | `centroid_angle_offset` | `three_atom_plane` | `molstar_geometry` |
| Pi-pi | `centroid_angle_offset` | `least_squares` | unchanged |

The reusable site recognizer receives descriptive elemental/SMARTS names too.
Profiles specify complete behavior, including ordered normals, chemical
recognition, inclusive/strict comparisons and degeneracy handling. A descriptive
family name alone never establishes numerical equivalence.

The established `get_buch_hbonds` function keeps its name and tuple output;
its result describes `hydrogen_acceptor_distance`. No unverified paper is
assigned to the historical Buch label. The established spelling of
`get_luzard_chandler_hbonds` is retained for compatibility; new attribution
metadata spells the authors' name `luzar_chandler`.

## Why

A reference implementation is evidence for behavior, not proof of authorship.
The accepted policy uses known author names with verified references, otherwise
descriptive names and explicit software provenance.

## What is measured and what is assumed

The 511-test interaction/recognizer/scientific-control selection passed, including
canonical-versus-alias parity, incompatible profiles, prior independent scientific
controls, periodic images and persistence. Sixty-three doctest examples across
eight public modules passed. Four revised Toolbox/site-recognizer notebooks ran;
Foundations, Cookbook and all four Module 38 paths reflect the contract.
The numerical kernels and existing source-specific controls remain unchanged.
No comparative scientific accuracy claim or novel discovery is made.

## What was refuted

Replacing every profile with one undifferentiated distance/angle method loses
recognition, numerical and periodic conventions. Removing reference metadata
loses reproducibility. Renaming historical persisted results would rewrite
the provenance of an earlier calculation.

## Scope and exclusions

Existing interaction detectors and hydrogen-bond site recognition. No new
interaction physics, thresholds, energy interpretation or numerical kernel.

## Acceptance criteria

- Canonical and compatibility calls produce the same occurrences and measures.
- Invalid method/profile combinations fail clearly.
- Defaults keep their existing scientific behavior.
- Canonical identities survive typed and H5MSM round trips.
- API docstrings, User Guide, Cookbook and all four course paths agree.
