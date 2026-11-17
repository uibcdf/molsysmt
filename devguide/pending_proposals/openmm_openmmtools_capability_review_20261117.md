---
summary: Review reusable capabilities in the OpenMM and OpenMMTools source trees
issue: uibcdf/molsysmt#12
status: partial
opened: 2026-11-17
closed:
verification: measured
area: [api]
guard:
normative:
blocked_by: []
supersedes: []
---

# OpenMM and OpenMMTools capability review

The requested OpenMM/OpenMMTools study is complete. Issue #12 also covers other
libraries, so the broader inventory remains open. The main finding is a
reproduced error in an existing MolSysMT API
([#773](../pending_bugs/potential_energy_decomposition_drops_terms_and_ignores_live_openmm_context_state.md)).
The clearest new reusable operation is an explicit periodic-cell basis conversion
([#774](support_explicit_periodic_cell_basis_conversion_for_openmm_export.md)).

## Sources and limits

Both reference checkouts were clean when inspected on 2026-11-17. The MolSysMT
comparison used `a57f4c51b4feafc54cad2677c862cae85c4e2534`. OpenMM source
observations refer to `ba0aa236ac4d07241382869604c4d2ea58c4f3f5`. OpenMMTools
source observations refer to `a42cbdc862a0a4fe996a579dd1b04611ce9916a4`. The two
local checks used the installed OpenMM 8.6.1, and the cell check loaded the
pinned source function explicitly. Each check was a small static witness.
The reviewed OpenMM Python files carry permissive notices, and OpenMMTools
uses the [MIT license](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/LICENSE).
This study uses source concepts. Any later code reuse must retain applicable
notices and identify its source. Scientific attribution must distinguish
original methods, adaptations and software actually executed.

## OpenMM comparison

| Operation and inspected source | MolSysMT fit and users | Contract and evidence needed |
| --- | --- | --- |
| Convert cell lengths and angles to vectors and back. [`internal/unitcell.py`](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/openmm/app/internal/unitcell.py) | Reuse `pbc.get_box_from_lengths_and_angles`, `get_lengths_and_angles_from_box` and `get_volume_from_box` for general analysis and visualization. Native construction preserves the requested cell geometry and accepts per-structure quantities. | Existing analytical tests cover lengths, angles and volumes in `tests/scientific_truth/pbc/test_box_geometry.py`. Engine-specific reduction changes the basis-derived lengths and angles. A comparison must account for that distinction. |
| Reduce a triangular cell basis. [`reducePeriodicBoxVectors`](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/openmm/app/internal/unitcell.py#L81) | Investigate #774 after 1.0. `pbc` can own the reusable basis transformation and existing OpenMM adapters can own the engine boundary. Useful for crystallographic inputs and systems already rotated by an analysis or visual workflow. | The tested 30-degree cell is rejected by direct export and accepted after subtracting `a` from `b`. General delivery needs an integer basis map, a separate rotation policy, per-structure units, vector/image handling and lattice/coordinate checks. A handful of deterministic cells can qualify the initial scope. [OpenMM periodic box requirements](https://docs.openmm.org/latest/userguide/theory/05_other_features.html#periodic-boundary-conditions). |
| Element lookup by symbol, atomic number or nearest mass. [`element.py`](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/openmm/app/element.py) | Reuse `element.atom.normalize_atom_types` and `physchem.get_mass`. An exact atomic-number lookup could consolidate format-local tables if a consumer needs it. Avoid mass-based identification by default because force-field masses and isotopes may differ from reference weights. | Keep element symbols, isotope mass numbers, standard weights and stored particle masses distinct. Test the selected versioned table, invalid or missing values and vector ordering. This is a small lookup task independent of OpenMM installation. [CIAAW atomic weights](https://www.ciaaw.org/atomic-weights.htm). |
| List internal and external bonds, add standard and disulfide bonds. [`topology.py`](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/openmm/app/topology.py) | Reuse `ChemicalStates.get_bonds`, `chemical_states.get_bondgraph`, `build.get_covalent_bond_candidates` and the disulfide detector/build paths. A new bond filter would need a repeatable consumer workload. Preserve the distinction between a candidate and a stored declaration. | Evidence should check source atom or group indices, chemical-state scope and exact endpoint membership. OpenMM's proximity-based CYS rule is a heuristic, with a fixed cutoff and ordering. Avoid importing it as chemical authority. Small declared graphs are sufficient. |
| Place hydrogens and build solvent or membrane environments. [`modeller.py`](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/openmm/app/modeller.py) | Reuse `build.add_missing_hydrogens`, protonation assessment, native water/ion tools and `build.solvate`. Review the existing hydrogen refinement route under #323 and uibcdf/praxis#3. Take membrane assembly, solvation and equilibration to a concrete protocol review with Praxis when needed. | Keep chosen states, coordinate/atom maps and engine/force-field assumptions explicit. Model-specific placement needs independent geometry and conservation checks. Membrane equilibration requires separate scientific/resource review beyond the static fixtures in this study. [OpenMM model building guide](https://docs.openmm.org/latest/userguide/application/03_model_building_editing.html). |
| Add or remove extra particles to match force-field templates. [`Modeller.addExtraParticles`](https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/wrappers/python/openmm/app/modeller.py#L1113) | Investigate only for a declared water or mechanics consumer. Transporting types or positions and preserving a virtual-site construction rule are distinct capabilities. `build` can own explicit construction and `molecular_mechanics` can own parameterized particle roles. Native chemical-state assignments should keep their current ownership. | Define which particles are represented in the molecular inventory, dependency/weight data, per-structure coordinates, source maps and the persistence or refusal contract. Start from one template with an analytical weighted-position oracle and compare a small OpenMM fixture. Virtual sites, lone pairs and Drude particles have different semantics. [OpenMM virtual sites](https://docs.openmm.org/latest/userguide/theory/05_other_features.html#virtual-sites). |

## OpenMMTools comparison

| Operation and inspected source | MolSysMT fit and users | Contract and evidence needed |
| --- | --- | --- |
| Inspect forces and select compatible energy groups. [`forces.py`](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/openmmtools/forces.py#L54) and [`ThermodynamicState.reduced_potential_at_states`](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/openmmtools/states.py#L912) | `molecular_mechanics.get_model_recipe` already exposes effective model controls, and `get_potential_energy` has per-term output. Prioritize #773. Force identity and the live Hamiltonian matter for any future decomposition or reuse. | Three two-particle checks demonstrate duplicate-label loss, the use of default box and parameters, and source mutation. Validate each force term analytically, total agreement, original ownership, active box/parameters and qualified refusal of unsupported context state. Use the existing OpenMM route. |
| Radial harmonic and flat-bottom restraints on atoms or centers. [`RadiallySymmetricRestraintForce`](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/openmmtools/forces.py#L234) | MolSysMT already has OpenMM point and plane restraints, pinning and harmonic bond helpers. An engine-neutral two-group restraint could fill a gap once a workflow needs it. Keep standard-state corrections in the BindingMT scientific owner with protocol choices registered in Praxis. | Specify center weights, participant membership, dimensions of force constants and the periodic image used for both centers. Use two analytical groups and finite-difference force checks. A correction also requires explicit ensemble, standard concentration and integration assumptions. |
| Switched reaction-field variants. [`UnshiftedReactionFieldForce` and `SwitchedReactionFieldForce`](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/openmmtools/forces.py#L1110) | `get_model_recipe` inspects the OpenMM reaction-field settings and `get_non_bonded_potential_energy` has a bounded parity scope. A separate variant changes the physical model. Defer until requested by a protocol or user. | Validate energies and gradients across the switching region, exclusions, cutoff and PBC, and identify which published formulation is used. Standard cutoff electrostatics and these variants require separately reported assumptions. [OpenMM cutoff electrostatics](https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#coulomb-interaction-with-cutoff). |
| Snapshot a configuration and evaluate reduced potentials across states. [`states.py`](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/openmmtools/states.py) | `Structures`, `MolecularMechanics` and the OpenMM adapters supply geometry and model pieces. The OpenMMTools thermodynamic state has ensemble parameters with separate semantics from MolSysMT chemical states. BindingMT owns binding free-energy methods, Praxis owns protocol registration, and Nextia owns project/run orchestration. | A concrete consumer could request a reusable reduced-energy primitive. It would require dimensionless output, temperature, the configuration's volume for pressure coupling and separate configuration/model/state axes. Compare analytical `U/(RT)` and `(U+pV)/(RT)` with consistent molar units. Review the original statistical target before adding ensembles. [Shirts and Chodera, 2008](https://doi.org/10.1063/1.2978177), cited in the reviewed source. |
| Reuse contexts with compatible systems and integrators. [`cache.ContextCache`](https://github.com/choderalab/openmmtools/blob/a42cbdc862a0a4fe996a579dd1b04611ce9916a4/openmmtools/cache.py#L214) | Retain this as a design reference for an owned evaluator if repeated context construction measures as costly. Global caches would complicate model edits, cancellation, platform/device ownership and resource control. Take orchestration reuse to the caller with the actual workload. | Require reset and compatibility tests for box, positions, parameters, platform properties and integrator state. Measure context creation, reuse and peak CPU/device memory. Apply capacity and lifetime bounds. [OpenMMTools ContextCache contract](https://openmmtools.readthedocs.io/en/stable/api/generated/openmmtools.cache.ContextCache.html). |

## Priority

1. Fix and verify #773 on supported public routes before 1.0. It can silently
   return an incorrect analysis and modify a caller-owned engine system.
2. Keep #774 as an explicit targeted expansion. A small private adapter may
   suffice for one consumer. Promote a general lattice tool when its reusable
   contract and demand are clear.
3. Reuse the existing cell, mass, graph, solvent, ion and preparation tools.
   Revisit exact atomic-number lookup, virtual-site interchange, group restraints
   or local evaluator reuse only with a concrete consumer and an independent
   validation fixture.
4. Route ensemble protocols, standard-state corrections, free-energy workflows
   and execution policy to their scientific and orchestration owners. The
   existing OpenMMTools dependency disposition remains in
   [#524's record](runtime_dependency_api_floors.md).

The two local witnesses distinguish a correctness issue from an interoperability
proposal. Claims in other rows are source comparisons. Performance, cross-engine
scientific equivalence and installed release compatibility require separate evidence.
