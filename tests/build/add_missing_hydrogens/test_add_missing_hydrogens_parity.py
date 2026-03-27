"""
Parity tests for add_missing_hydrogens: MolSysMT engine vs PDBFixer engine.

Known difference between engines:
  - engine='PDBFixer' calls addMissingHydrogens(pH=7.4) which uses OpenMM
    protonation-state prediction (ASP, GLU deprotonated; HIS tautomer
    assignment; C-terminal COOH protonated as per pH).
  - engine='MolSysMT' adds all hydrogens from the topology database without
    protonation-state assignment (standard protonation everywhere).
  - engine='MolSysMT' currently skips non-standard groups (ACE, NME) and free
    termini are treated differently from PDBFixer at pH 7.4 (OXT+HXT handling).

For a neutral, internal (non-terminal) residue like VAL in AlaValPro the two
engines are expected to agree on the exact H count.  For real proteins with
ionisable residues the counts will differ; the tests check only that:
  1. Both engines add H atoms (count increases).
  2. Every H is bonded to at least one heavy atom.
  3. The H count from the MolSysMT engine is within ±15 % of the PDBFixer
     count (gross disagreement would indicate a structural bug, not a pH
     model difference).
"""

import pytest
import molsysmt as msm


@pytest.fixture(scope='module')
def avp_heavy():
    """AlaValPro heavy-only (all H removed).

    Free-terminus tripeptide: no capping groups, so both engines process the
    same atoms.  OXT/HXT terminal differences are confined to the terminal
    residues; internal VAL (group_index==1) is unaffected.
    """
    mol = msm.build.build_peptide('AlaValPro', engine='MolSysMT',
                                   to_form='molsysmt.MolSys')
    return msm.remove(mol, selection='atom_type=="H"')


@pytest.fixture(scope='module')
def avp_full():
    """AlaValPro as built (has H atoms)."""
    return msm.build.build_peptide('AlaValPro', engine='MolSysMT',
                                   to_form='molsysmt.MolSys')


@pytest.fixture(scope='module')
def trpcage_heavy():
    """Trp-Cage (20 residues, ~300 atoms) — large enough to test real-protein behaviour
    but small enough that PDBFixer+OpenMM finishes in a few seconds."""
    mol = msm.convert(msm.systems['Trp-Cage']['1l2y.h5msm'])
    mol = msm.build.add_missing_heavy_atoms(mol, engine='MolSysMT')
    return msm.remove(mol, selection='atom_type=="H"')


# ── Neutral peptide: internal residue exact count agreement ───────────────────

def test_parity_internal_residue_h_count(avp_heavy, avp_full):
    """Both engines add exactly the same H atoms to the internal VAL residue.

    group_index==1 (VAL) is not a terminal residue — no OXT/HXT or protonation
    ambiguity — so both engines must agree on its H count.
    """
    n_h_expected = msm.get(avp_full, element='atom',
                            selection='group_index==1 and atom_type=="H"', n_atoms=True)
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_hydrogens(avp_heavy, engine=eng)
        n_h = msm.get(r, element='atom',
                       selection='group_index==1 and atom_type=="H"', n_atoms=True)
        assert n_h == n_h_expected, (
            f"{eng}: internal VAL H count {n_h} != expected {n_h_expected}"
        )


def test_parity_neutral_peptide_h_increases(avp_heavy):
    """Both engines add at least some H atoms to the heavy-only peptide."""
    n_heavy = msm.get(avp_heavy, n_atoms=True)
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_hydrogens(avp_heavy, engine=eng)
        assert msm.get(r, n_atoms=True) > n_heavy, f"{eng}: no atoms added"


def test_parity_neutral_peptide_group_names(avp_heavy):
    """Group names unchanged by both engines."""
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_hydrogens(avp_heavy, engine=eng)
        assert msm.get(r, element='group', group_name=True) == ['ALA', 'VAL', 'PRO']


# ── All H bonded to heavy atoms ───────────────────────────────────────────────

def test_parity_neutral_peptide_h_bonded_native(avp_heavy):
    """Every H atom added by MolSysMT engine is bonded to a heavy atom."""
    r = msm.build.add_missing_hydrogens(avp_heavy, engine='MolSysMT')
    topo = r.topology
    bonded = set()
    for _, row in topo.bonds.iterrows():
        bonded.add(int(row['atom1_index']))
        bonded.add(int(row['atom2_index']))
    h_indices = topo.atoms[topo.atoms['atom_type'] == 'H'].index.tolist()
    assert all(i in bonded for i in h_indices)


def test_parity_neutral_peptide_h_bonded_pdbfixer(avp_heavy):
    """Every H atom added by PDBFixer engine is bonded to a heavy atom."""
    r = msm.build.add_missing_hydrogens(avp_heavy, engine='PDBFixer')
    topo = r.topology
    bonded = set()
    for _, row in topo.bonds.iterrows():
        bonded.add(int(row['atom1_index']))
        bonded.add(int(row['atom2_index']))
    h_indices = topo.atoms[topo.atoms['atom_type'] == 'H'].index.tolist()
    assert all(i in bonded for i in h_indices)


# ── Real protein: count within tolerance ─────────────────────────────────────

def test_parity_protein_h_counts_within_tolerance(trpcage_heavy):
    """For a real protein, MolSysMT and PDBFixer H counts agree within 15 %.

    PDBFixer uses protonation-state prediction (pH 7.4), so small differences
    are expected (ASP/GLU deprotonated, HIS tautomers).  A >15 % difference
    would indicate a structural bug.
    """
    r_native = msm.build.add_missing_hydrogens(trpcage_heavy, engine='MolSysMT')
    r_pdb    = msm.build.add_missing_hydrogens(trpcage_heavy, engine='PDBFixer')
    n_h_native = msm.get(r_native, element='atom', selection='atom_type=="H"', n_atoms=True)
    n_h_pdb    = msm.get(r_pdb,    element='atom', selection='atom_type=="H"', n_atoms=True)
    assert n_h_native > 0
    assert n_h_pdb > 0
    ratio = n_h_native / n_h_pdb
    assert 0.85 <= ratio <= 1.15, (
        f"H count ratio MolSysMT/PDBFixer = {ratio:.3f} outside [0.85, 1.15]: "
        f"native={n_h_native}, pdbfixer={n_h_pdb}"
    )


def test_parity_protein_heavy_count_unchanged(trpcage_heavy):
    """Adding H does not change the heavy atom count in either engine."""
    n_heavy_before = msm.get(trpcage_heavy, element='atom',
                              selection='atom_type!="H"', n_atoms=True)
    for eng in ('MolSysMT', 'PDBFixer'):
        r = msm.build.add_missing_hydrogens(trpcage_heavy, engine=eng)
        n_heavy_after = msm.get(r, element='atom',
                                 selection='atom_type!="H"', n_atoms=True)
        assert n_heavy_after == n_heavy_before, f"{eng}: heavy atom count changed"
