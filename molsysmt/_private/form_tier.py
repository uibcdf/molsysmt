"""Support-tier mapping for MolSysMT forms.

Only Tier 2 and Tier 3 forms are listed here.  Tier 1 forms produce no runtime
signal, so they are omitted.  Unregistered forms are treated as Tier 1 by the
SupportTierRegistry (i.e., silence).

Tier semantics
--------------
- Tier 1 (contractual): regressions are patch-priority; API is stable for 1.x.
- Tier 2 (best-effort): supported and maintained, but not contractually
  guaranteed for all workflows.  Emits a WARNING once per form per session.
- Tier 3 (experimental / niche): available but outside the contractual 1.0.0
  core.  Emits an INFO once per form per session.

See devguide/support_tiers.ipynb for the authoritative tier classification.
"""

from __future__ import annotations

#: Mapping from form name to support tier (2 or 3).
#: Tier 1 forms are not listed; absence from this dict implies Tier 1.
FORM_TIERS: dict[str, int] = {

    # ------------------------------------------------------------------
    # Tier 2 — best-effort
    # ------------------------------------------------------------------
    "file:mmtf":                   2,
    "mmtf.MMTFDecoder":            2,
    "biopython.Seq":               2,
    "biopython.SeqRecord":         2,
    "file:h5":                     2,
    "molsysmt.CIFFileHandler":     2,
    "molsysmt.GROFileHandler":     2,
    "mdtraj.HDF5TrajectoryFile":   2,

    # ------------------------------------------------------------------
    # Tier 3 — experimental / niche
    # ------------------------------------------------------------------
    "parmed.Structure":            3,
    "rdkit.Mol":                   3,
    "biopython.PDBStructure":      3,
    "MDAnalysis.Universe":         3,
    "MDAnalysis.AtomGroup":        3,
    "MDAnalysis.Topology":         3,
    "pytraj.Trajectory":           3,
    "pytraj.Topology":             3,
    "file:fasta":                  3,
    "file:pir":                    3,
    "string:smiles":               3,
    "file:smi":                    3,
    "file:dcd":                    3,
    "file:mol2":                   3,
    "file:crd":                    3,
    "file:inpcrd":                 3,
    "file:prmtop":                 3,
    "file:psf":                    3,
    "file:gro":                    3,
    "file:trjpk":                  3,
    "mdtraj.DCDTrajectoryFile":    3,
    "mdtraj.XTCTrajectoryFile":    3,
    "molsysmt.MolecularMechanics": 3,
    "molsysmt.MolecularMechanicsDict": 3,
}


def check_form_tier(form_name: str) -> None:
    """Emit a support-tier signal for *form_name* if it is Tier 2 or Tier 3.

    Signals are deduplicated: each form name fires at most once per session
    regardless of how many times this function is called.

    Tier 1 forms (and any form not in :data:`FORM_TIERS`) produce no signal.
    """
    tier = FORM_TIERS.get(form_name)
    if tier is None:
        return
    from molsysmt._private.smonitor import bundle
    registry = bundle.tier_registry()
    if form_name not in registry._tiers:
        registry.register(form_name, tier)
    registry.check(form_name)
