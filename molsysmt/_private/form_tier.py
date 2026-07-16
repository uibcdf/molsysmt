"""Defining the explicit support tier for every MolSysMT form adapter.

Tier semantics
--------------
- Tier 1 (contractual): regressions are patch-priority; API is stable for 1.x.
- Tier 2 (best-effort): supported and maintained, but not contractually
  guaranteed for all workflows. Emits a warning once per form per session.
- Tier 3 (experimental / niche): available but outside the contractual 1.0.0
  core. Emits an info signal once per form per session.

Every adapter must appear in :data:`FORM_TIERS`. Unknown forms are registry
integrity failures; absence never implies Tier 1.
"""

from __future__ import annotations


_TIER_1_FORMS = (
    "MDAnalysis.topology.PDBParser",
    "XYZ",
    "cupy_ndarray",
    "file:bcif",
    "file:bcif.gz",
    "file:cif",
    "file:cif.gz",
    "file:h5msm",
    "file:mdcrd",
    "file:molsys_yaml",
    "file:pdb",
    "file:structures_yaml",
    "file:top",
    "file:topology_yaml",
    "file:xtc",
    "file:xyz",
    "file:xyznpy",
    "mdtraj.AmberRestartFile",
    "mdtraj.GroTrajectoryFile",
    "mdtraj.PDBTrajectoryFile",
    "mdtraj.Topology",
    "mdtraj.Trajectory",
    "mmcif.PdbxContainers.DataContainer",
    "molsysmt.H5MSMFileHandler",
    "molsysmt.MolSys",
    "molsysmt.MolSysBuilder",
    "molsysmt.MolSysDict",
    "molsysmt.PDBFileHandler",
    "molsysmt.Structures",
    "molsysmt.StructuresDict",
    "molsysmt.Topology",
    "molsysmt.TopologyDict",
    "molsysmt.ViewerJSON",
    "molsysviewer.MolSysView",
    "networkx.Graph",
    "nglview.NGLWidget",
    "openmm.AmberInpcrdFile",
    "openmm.AmberPrmtopFile",
    "openmm.CharmmCrdFile",
    "openmm.CharmmPsfFile",
    "openmm.Context",
    "openmm.GromacsGroFile",
    "openmm.GromacsTopFile",
    "openmm.Modeller",
    "openmm.PDBFile",
    "openmm.Simulation",
    "openmm.State",
    "openmm.System",
    "openmm.Topology",
    "parmed.GromacsTopologyFile",
    "pdbfixer.PDBFixer",
    "string:alphafold_id",
    "string:amino_acids_1",
    "string:amino_acids_3",
    "string:pdb_id",
    "string:pdb_text",
    "string:uniprot_id",
)

_TIER_2_FORMS = (
    "biopython.Seq",
    "biopython.SeqRecord",
    "file:h5",
    "mdtraj.HDF5TrajectoryFile",
    "molsysmt.CIFFileHandler",
    "molsysmt.GROFileHandler",
)

_TIER_3_FORMS = (
    "MDAnalysis.AtomGroup",
    "MDAnalysis.Topology",
    "MDAnalysis.Universe",
    "biopython.PDBStructure",
    "file:crd",
    "file:dcd",
    "file:fasta",
    "file:gro",
    "file:inpcrd",
    "file:mol2",
    "file:pir",
    "file:prmtop",
    "file:psf",
    "file:smi",
    "file:trjpk",
    "mdtraj.DCDTrajectoryFile",
    "mdtraj.XTCTrajectoryFile",
    "molsysmt.MolecularMechanics",
    "molsysmt.MolecularMechanicsDict",
    "openff.Molecule",
    "openff.Topology",
    "parmed.Structure",
    "pytraj.Topology",
    "pytraj.Trajectory",
    "rdkit.Mol",
    "string:smiles",
)

FORM_TIERS: dict[str, int] = {
    **dict.fromkeys(_TIER_1_FORMS, 1),
    **dict.fromkeys(_TIER_2_FORMS, 2),
    **dict.fromkeys(_TIER_3_FORMS, 3),
}


def get_form_tier(form_name: str) -> int | None:
    """Returning the explicitly registered tier for a form."""
    return FORM_TIERS.get(form_name)


def check_form_tier(form_name: str) -> None:
    """Emitting the explicitly registered support-tier signal for a form.

    Tier 1 forms produce no signal. Tier 2 and Tier 3 signals are deduplicated
    by SMonitor. An unknown form indicates drift between adapter discovery and
    the registry and therefore fails explicitly.
    """
    tier = get_form_tier(form_name)
    if tier is None:
        from molsysmt._private.smonitor import InternalAlgorithmError

        raise InternalAlgorithmError(
            reason=(
                f"Form '{form_name}' has no explicit support-tier entry. "
                "Register it in molsysmt._private.form_tier.FORM_TIERS."
            ),
            caller="molsysmt._private.form_tier.check_form_tier",
        )
    if tier == 1:
        return

    from molsysmt._private.smonitor import bundle

    registry = bundle.tier_registry()
    if form_name not in registry._tiers:
        registry.register(form_name, tier)
    registry.check(form_name)
