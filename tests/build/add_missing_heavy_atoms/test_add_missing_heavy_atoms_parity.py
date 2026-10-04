"""
Parity tests for add_missing_heavy_atoms: MolSysMT engine vs PDBFixer engine.

The native engine uses bounded template alignment and leaves unsupported gaps
unassessed. PDBFixer chooses its own reconstruction. Atom-count agreement is tested
only for an explicitly shared supported selection; native rejection and unchanged
observed poses are checked separately. See uibcdf/molsysmt#322.
"""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    UnassessedResidueWarning,
)


@pytest.fixture(scope="module")
def barnase_barstar():
    return msm.convert(msm.systems["Barnase-Barstar"]["1brs.bcif.gz"])


@pytest.fixture(scope="module")
def avp_no_cb():
    mol = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    return msm.remove(mol, selection='atom_name=="CB"')


# ── Barnase-Barstar (real PDB structure) ──────────────────────────────────────


def test_parity_1brs_total_atom_count(barnase_barstar):
    """Both engines reconstruct the four declared supported single-atom gaps."""
    selection = "group_index in [282, 325, 385, 587]"
    assert msm.build.get_missing_heavy_atoms(barnase_barstar, selection=selection) == {
        282: ["OG"],
        325: ["O"],
        385: ["NZ"],
        587: ["O"],
    }
    with pytest.warns(StructuralAttributeDropWarning):
        r_native = msm.build.add_missing_heavy_atoms(
            barnase_barstar, selection=selection, engine="MolSysMT"
        )
    r_pdb = msm.build.add_missing_heavy_atoms(
        barnase_barstar, selection=selection, engine="PDBFixer"
    )
    assert msm.get(r_native, n_atoms=True) == msm.get(r_pdb, n_atoms=True) == 5155


def test_parity_1brs_atoms_added(barnase_barstar):
    """Full reconstruction deliberately differs when the native method abstains."""
    with pytest.warns((UnassessedResidueWarning, StructuralAttributeDropWarning)):
        r_native = msm.build.add_missing_heavy_atoms(barnase_barstar, engine="MolSysMT")
    r_pdb = msm.build.add_missing_heavy_atoms(barnase_barstar, engine="PDBFixer")
    n_before = msm.get(barnase_barstar, n_atoms=True)
    delta_native = msm.get(r_native, n_atoms=True) - n_before
    delta_pdb = msm.get(r_pdb, n_atoms=True) - n_before
    assert delta_native == 4
    assert delta_pdb == 78


def test_parity_1brs_backbone_present_native(barnase_barstar):
    """Rejected multi-atom gaps retain their exact missing-atom inventories."""
    from molsysmt.build.get_missing_heavy_atoms import get_missing_heavy_atoms

    missing_before = get_missing_heavy_atoms(barnase_barstar, engine="MolSysMT")
    with pytest.warns((UnassessedResidueWarning, StructuralAttributeDropWarning)):
        r_native = msm.build.add_missing_heavy_atoms(barnase_barstar, engine="MolSysMT")
    missing_after = get_missing_heavy_atoms(r_native, engine="MolSysMT")
    assert missing_after == {
        i: names for i, names in missing_before.items() if i not in {282, 325, 385, 587}
    }


def test_parity_1brs_backbone_present_pdbfixer(barnase_barstar):
    """After PDBFixer fix, all residues that had missing atoms are now complete."""
    from molsysmt.build.get_missing_heavy_atoms import get_missing_heavy_atoms

    missing_before = get_missing_heavy_atoms(barnase_barstar, engine="MolSysMT")
    r_pdb = msm.build.add_missing_heavy_atoms(barnase_barstar, engine="PDBFixer")
    missing_after = get_missing_heavy_atoms(r_pdb, engine="MolSysMT")
    assert set(missing_after.keys()).isdisjoint(set(missing_before.keys()))


# ── Synthetic: AlaValPro with CB removed ─────────────────────────────────────


def test_parity_synthetic_atom_count(avp_no_cb):
    """The native geometry gate rejects a conflicting VAL template placement."""
    with pytest.warns(
        (UnassessedResidueWarning, StructuralAttributeDropWarning)
    ) as caught:
        r_native = msm.build.add_missing_heavy_atoms(avp_no_cb, engine="MolSysMT")
    assert any("VAL" in str(w.message) and "geometry" in str(w.message) for w in caught)
    r_pdb = msm.build.add_missing_heavy_atoms(avp_no_cb, engine="PDBFixer")
    assert msm.get(r_native, n_atoms=True) == msm.get(avp_no_cb, n_atoms=True) + 2
    assert msm.get(r_pdb, n_atoms=True) == msm.get(avp_no_cb, n_atoms=True) + 3


def test_parity_synthetic_cb_present(avp_no_cb):
    """The exact unresolved native atom remains explicit, not silently completed."""
    for eng in ("MolSysMT", "PDBFixer"):
        r = msm.build.add_missing_heavy_atoms(avp_no_cb, engine=eng)
        n_cb = msm.get(r, element="atom", selection='atom_name=="CB"', n_atoms=True)
        assert n_cb == (2 if eng == "MolSysMT" else 3)
        assert msm.build.get_missing_heavy_atoms(r) == (
            {1: ["CB"]} if eng == "MolSysMT" else {}
        )


def test_parity_synthetic_group_names_unchanged(avp_no_cb):
    """Group names are not altered by either engine."""
    for eng in ("MolSysMT", "PDBFixer"):
        r = msm.build.add_missing_heavy_atoms(avp_no_cb, engine=eng)
        names = msm.get(r, element="group", group_name=True)
        assert names == ["ALA", "VAL", "PRO"], f"{eng}: {names}"
