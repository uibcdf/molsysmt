---
summary: Define faithful OpenMM runtime and State snapshot copy contracts.
issue: uibcdf/molsysmt#592
status: open
opened: 2026-11-05
closed:
verification: inspected
area: [api, form, docs, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Engine runtime and captured-snapshot copying

What — define faithful independent-copy contracts for the existing openmm.Context, openmm.Simulation and openmm.State forms, then implement supported cases in their owning adapters and reuse them through basic.copy.

How — OpenMM primary source distinguishes partially captured State fields from a live runtime. Context.setState does not restore all internal state (notably RNGs); checkpoints contain more but depend on model/platform/hardware/version. OpenMM TestPickle separately exercises System, Integrator and State serialization. Native copy adapters currently reject all three forms. #588 fixes minimization safety by invoking that copy boundary before any independent engine optimization, not by inventing a partial clone.

Why — independent snapshots and runtimes are reusable tools for analysis/preparation beyond minimization. Coordinate-only reconstruction must not silently replace an executed physical model, platform or dynamic state. A Simulation also has topology and workflow/reporters that require explicit ownership decisions.

Acceptance — specify snapshot versus runtime fidelity, captured/absent State fields, System/Context synchronization, model/force parameters, current globals/box/positions/velocities/time/step, integrator internals and platform properties. Define reporter/Python-subclass ownership and checkpoint compatibility; reject unsupported cases before modifying input, without engine/model/platform fallback. Preserve units and mappings. Implement only qualified supported cases in the form adapters with independent mutation and partial-State guards, including actual CPU/Reference execution; GPU/platform coverage must be separately qualified. Align basic.copy, form capability claims, User Guide/course and optional scientific attribution where applicable.

Scope — separate follow-up, not a requirement or release waiver for #588's fail-before-optimization correction. Propose after the current pre-1.0 safety queue unless a consumer establishes a concrete earlier requirement. Existing State/Context/Simulation names and forms are reused; no placeholder form or minimizer-local copy implementation is requested.

Reference — https://github.com/openmm/openmm/blob/ba0aa236ac4d07241382869604c4d2ea58c4f3f5/openmmapi/include/openmm/Context.h and wrappers/python/tests/TestPickle.py at that revision.

Record — devguide/pending_proposals/define_faithful_openmm_runtime_and_state_snapshot_copy_contracts.md
Related — #588, #582 and #567.

## Intended timing and owner

The owning implementation modules are the existing form adapters, not molecular
mechanics orchestration. General consumers reuse basic.copy. Schedule after the
current safety stabilization unless an actual consumer requirement changes that
priority. No independent Context/Simulation/State copy is implemented by #588;
its capability/error documentation is corrected to match actual behavior.
