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
    "MDAnalysis.Universe":         2,
    "MDAnalysis.AtomGroup":        2,
    "MDAnalysis.Topology":         2,
    "openmm.Modeller":             2,
    "openmm.Context":              2,
    "openmm.Simulation":           2,
    "rdkit.Mol":                   2,
    "biopython.PDBStructure":      2,
    "parmed.Structure":            2,
    "molsysviewer.MolSysView":     2,
    "nglview.NGLWidget":           2,
    # string:pdb_id and string:alphafold_id promoted to Tier 1 — omitted here

    # ------------------------------------------------------------------
    # Tier 3 — experimental / niche
    # ------------------------------------------------------------------
    "networkx.Graph":              3,
    "pytraj.Trajectory":           3,
    "pytraj.Topology":             3,
    "biopython.Seq":               3,
    "biopython.SeqRecord":         3,
    "XYZ":                         3,
    "file:mmtf":                   3,
    "file:dcd":                    3,
    "file:mol2":                   3,
    "file:crd":                    3,
    "file:inpcrd":                 3,
    "file:prmtop":                 3,
    "file:psf":                    3,
    "file:gro":                    3,
    "file:h5":                     3,
    "file:trjpk":                  3,
    "file:msmpk":                  3,
    "file:xyznpy":                 3,
    "file:cif":                    3,
    "file:cif.gz":                 3,
    "mmcif.PdbxContainers.DataContainer": 3,
    "mmtf.MMTFDecoder":            3,
    "openmm.AmberInpcrdFile":      3,
    "openmm.AmberPrmtopFile":      3,
    "openmm.CharmmCrdFile":        3,
    "openmm.CharmmPsfFile":        3,
    "openmm.GromacsGroFile":       3,
    "openmm.GromacsTopFile":       3,
    "openmm.PDBFile":              3,
    "openmm.State":                3,
    "openmm.System":               3,
    "pdbfixer.PDBFixer":           3,
    "string:amino_acids_1":        3,
    "string:amino_acids_3":        3,
    "string:pdb_text":             3,
    "mdtraj.DCDTrajectoryFile":    3,
    "mdtraj.HDF5TrajectoryFile":   3,
    "mdtraj.XTCTrajectoryFile":    3,
    "molsysmt.CIFFileHandler":     3,
    "molsysmt.GROFileHandler":     3,
    "molsysmt.MolecularMechanics": 3,
    "molsysmt.MolecularMechanicsDict": 3,
    "molsysmt.ViewerJSON":         3,
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
