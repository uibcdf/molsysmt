# Support Tier Protocol — MolSysMT Integration

## What was implemented

In March 2026, MolSysMT adopted the **support-tier protocol** introduced in SMonitor as
part of the MolSysSuite 1.0.0 stabilization effort.  The protocol communicates to users
which parts of the API carry a formal support guarantee at runtime, using structured
SMonitor diagnostics rather than ad-hoc comments or docstrings.

See `smonitor/devguide/support_tier_protocol.md` for the authoritative protocol
specification.  This document covers the MolSysMT-specific choices.

---

## Tier semantics (recap)

| Tier | Meaning | Runtime signal |
|------|---------|----------------|
| **1** — Contractual | Regressions are patch-priority; API is stable for 1.x | None |
| **2** — Best-effort | Supported and maintained but not contractually guaranteed | `WARNING` once per form/function per session |
| **3** — Experimental / niche | Available but outside the contractual 1.0.0 core | `INFO` once per form/function per session |

---

## Form classification

Forms are classified in `molsysmt/_private/form_tier.py`.  Only Tier 2 and Tier 3
forms are listed there; absence from the dict implies Tier 1 (silence).

### Tier 1 (contractual, not listed)

`molsysmt.MolSys`, `molsysmt.Topology`, `molsysmt.Structures`,
`molsysmt.MolSysBuilder`, `molsysmt.MolSysDict`, `molsysmt.TopologyDict`,
`molsysmt.StructuresDict`, `file:h5msm`, `file:molsys_yaml`, `file:topology_yaml`,
`file:structures_yaml`, `file:bcif`, `file:bcif_gz`, `openmm.Topology`,
`mdtraj.Trajectory`, `mdtraj.Topology`, `file:pdb`, `file:xtc`.

### Tier 2 — best-effort (13 forms)

`MDAnalysis.Universe`, `MDAnalysis.AtomGroup`, `MDAnalysis.Topology`,
`openmm.Modeller`, `openmm.Context`, `openmm.Simulation`, `rdkit.Mol`,
`biopython.PDBStructure`, `parmed.Structure`, `molsysviewer.MolSysView`,
`nglview.NGLWidget`, `string:pdb_id`, `string:alphafold_id`.

### Tier 3 — experimental / niche (~42 forms)

`networkx.Graph`, `pytraj.Trajectory`, `pytraj.Topology`, `biopython.Seq`,
`biopython.SeqRecord`, `XYZ`, `file:mmtf`, `file:dcd`, `file:mol2`, `file:crd`,
`file:inpcrd`, `file:prmtop`, `file:psf`, `file:gro`, `file:h5`, `file:trjpk`,
`file:msmpk`, `file:xyznpy`, `file:cif`, `file:cif.gz`,
`mmcif.PdbxContainers.DataContainer`, `mmtf.MMTFDecoder`,
`openmm.AmberInpcrdFile`, `openmm.AmberPrmtopFile`, `openmm.CharmmCrdFile`,
`openmm.CharmmPsfFile`, `openmm.GromacsGroFile`, `openmm.GromacsTopFile`,
`openmm.PDBFile`, `openmm.State`, `openmm.System`, `pdbfixer.PDBFixer`,
`string:amino_acids_1`, `string:amino_acids_3`, `string:pdb_text`,
`mdtraj.DCDTrajectoryFile`, `mdtraj.HDF5TrajectoryFile`, `mdtraj.XTCTrajectoryFile`,
`molsysmt.CIFFileHandler`, `molsysmt.GROFileHandler`, `molsysmt.MolecularMechanics`,
`molsysmt.MolecularMechanicsDict`, `molsysmt.ViewerJSON`.

---

## Function classification

### Tier 3 functions (decorated with `@support_tier(3)`)

- `molsysmt.molecular_dynamics.run_NPT_equilibration`
- `molsysmt.molecular_dynamics.run_NVT_equilibration`

The entire `molecular_dynamics` module is outside the contractual 1.0.0 core.
Individual functions are decorated rather than the module to keep the signal granular.

---

## How the hook works

`molsysmt/basic/get_form.py` is the single hook point for form tier signals.
Every public MolSysMT API function calls `get_form()` to resolve the input form,
so placing `check_form_tier(output)` there ensures the signal fires exactly once
per form per session regardless of which public function the user called.

```python
# get_form.py (simplified)
from molsysmt._private.form_tier import check_form_tier

def get_form(molecular_system):
    ...
    check_form_tier(output)   # emits WARNING/INFO at most once per session
    return output
```

`check_form_tier()` lazily registers the form with the bundle's `SupportTierRegistry`
and calls `registry.check()`, which deduplicates via `DiagnosticBundle._tier_dedup_cache`.

---

## SMonitor catalog entries

Two new entries were added to `molsysmt/_private/smonitor/catalog.py`:

| Catalog key | Code | Level | Purpose |
|---|---|---|---|
| `SupportTier2Warning` | `MSM-WARN-TIER-002` | WARNING | Tier 2 form/function used |
| `SupportTier3Info` | `MSM-INFO-TIER-003` | INFO | Tier 3 form/function used |

The CODES dict provides multi-profile messages (developer, user, debug) for both codes,
plus a revised `MSM-INFO-EXP-001` entry for the legacy `ExperimentalPath` catalog key.

---

## How to use `support_tier` in MolSysMT modules

```python
from molsysmt._private.smonitor import support_tier

@support_tier(3)
def my_experimental_function(...):
    ...
```

`support_tier` is exported from `molsysmt._private.smonitor` alongside `experimental`
(which is now an alias for `support_tier(3)`).

---

## What remains pending / future ideas

- **Function-level Tier 2**: no MolSysMT functions are currently classified Tier 2, but
  `@support_tier(2)` is available if needed.
- **`molecular_dynamics` module expansion**: if more functions are added to this module,
  apply `@support_tier(3)` to each.
- **Tier 1 function audit**: explicitly document which public API functions are Tier 1
  (currently implicit — all decorated functions not using `@support_tier` are Tier 1 by
  silence).
- **Auto-population of form tiers from module attributes**: if each form module exposed
  a `form_tier: int` attribute, `check_form_tier()` could look it up dynamically instead
  of consulting a centralized dict.  This would eliminate the need to update
  `form_tier.py` when adding a new form.
- **`support_tier` as a module-level decorator**: for marking entire sub-packages (e.g.,
  `molecular_dynamics`) as Tier 3 without decorating every function individually.
- **CLI / session report**: a `smonitor report` section listing Tier 2/3 items used in
  a session would help QA and support workflows.
