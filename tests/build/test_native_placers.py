"""
Unit tests for molsysmt/build/_native_placers.py.

Each public helper is tested in isolation with minimal fixtures so that
failures point directly to the function at fault, independently of the
higher-level add_missing_heavy_atoms / add_missing_terminal_cappings tests.
"""

import pytest
import numpy as np
import pandas as pd

from molsysmt.build._native_placers import (
    load_residue_template,
    _sort_bonds_inplace,
    place_missing_in_group,
    append_atoms_to_molsys,
    place_ace_group,
    place_nme_group,
    rebuild_molsys_with_new_groups,
    _normalize,
    _perpendicular_component,
)


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def ala_template():
    return load_residue_template("ALA")


@pytest.fixture(scope="module")
def ace_template():
    return load_residue_template("ACE")


@pytest.fixture(scope="module")
def nme_template():
    return load_residue_template("NME")


@pytest.fixture(scope="module")
def aaa_molsys():
    import molsysmt as msm
    return msm.build.build_peptide("AAA", engine="MolSysMT", to_form="molsysmt.MolSys")


# ---------------------------------------------------------------------------
# load_residue_template
# ---------------------------------------------------------------------------

class TestLoadResidueTemplate:

    def test_known_residue_returns_dict(self, ala_template):
        assert isinstance(ala_template, dict)

    def test_has_required_keys(self, ala_template):
        assert "atoms" in ala_template
        assert "coords_nm" in ala_template
        assert "bonds" in ala_template

    def test_atoms_is_list_of_strings(self, ala_template):
        assert isinstance(ala_template["atoms"], list)
        assert all(isinstance(a, str) for a in ala_template["atoms"])

    def test_coords_shape_matches_atoms(self, ala_template):
        coords = np.asarray(ala_template["coords_nm"])
        assert coords.shape == (len(ala_template["atoms"]), 3)

    def test_bonds_are_pairs_of_names(self, ala_template):
        for b in ala_template["bonds"]:
            assert len(b) == 2
            assert b[0] in ala_template["atoms"]
            assert b[1] in ala_template["atoms"]

    def test_unknown_residue_returns_none(self):
        assert load_residue_template("NOTARESIDUE") is None

    def test_result_is_cached(self, ala_template):
        second = load_residue_template("ALA")
        assert second is ala_template   # same object — cache hit


# ---------------------------------------------------------------------------
# _sort_bonds_inplace
# ---------------------------------------------------------------------------

class TestSortBondsInplace:

    def _make_bonds_df(self, pairs):
        df = pd.DataFrame(pairs, columns=["atom1_index", "atom2_index"])
        df["atom1_index"] = df["atom1_index"].astype("Int64")
        df["atom2_index"] = df["atom2_index"].astype("Int64")
        return df

    def test_flips_reversed_pairs(self):
        df = self._make_bonds_df([(5, 2), (0, 3)])
        _sort_bonds_inplace(df)
        assert df.loc[0, "atom1_index"] <= df.loc[0, "atom2_index"]
        assert df.loc[1, "atom1_index"] <= df.loc[1, "atom2_index"]

    def test_sorted_by_atom1_then_atom2(self):
        df = self._make_bonds_df([(3, 4), (1, 2), (1, 0)])
        _sort_bonds_inplace(df)
        a1 = df["atom1_index"].tolist()
        a2 = df["atom2_index"].tolist()
        assert a1 == sorted(a1)   # primary sort
        # within same a1, a2 must be sorted too
        for i in range(len(a1) - 1):
            if a1[i] == a1[i + 1]:
                assert a2[i] <= a2[i + 1]

    def test_index_is_reset(self):
        df = self._make_bonds_df([(9, 1), (3, 0)])
        _sort_bonds_inplace(df)
        assert list(df.index) == list(range(len(df)))


# ---------------------------------------------------------------------------
# _normalize and _perpendicular_component (private geometry helpers)
# ---------------------------------------------------------------------------

class TestGeometryHelpers:

    def test_normalize_unit_length(self):
        v = np.array([3.0, 4.0, 0.0])
        n = _normalize(v)
        assert abs(np.linalg.norm(n) - 1.0) < 1e-10

    def test_normalize_zero_returns_none(self):
        assert _normalize(np.zeros(3)) is None

    def test_perpendicular_component_is_orthogonal(self):
        vec  = np.array([1.0, 1.0, 0.0])
        axis = np.array([1.0, 0.0, 0.0])
        perp = _perpendicular_component(vec, axis)
        assert abs(np.dot(perp, axis)) < 1e-12

    def test_perpendicular_component_parallel_is_zero(self):
        vec  = np.array([2.0, 0.0, 0.0])
        axis = np.array([1.0, 0.0, 0.0])
        perp = _perpendicular_component(vec, axis)
        assert np.linalg.norm(perp) < 1e-12


# ---------------------------------------------------------------------------
# place_missing_in_group
# ---------------------------------------------------------------------------

class TestPlaceMissingInGroup:

    def test_returns_dict_with_placed_atom(self, aaa_molsys, ala_template):
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        # Remove CB from the system
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        topo = molsys_no_cb.topology
        coords = puw.get_value(molsys_no_cb.structures.coordinates, to_unit="nm")
        result = place_missing_in_group(topo, coords, group_idx=0,
                                        missing_names=["CB"], template=ala_template)
        assert "CB" in result

    def test_coords_shape_is_n_structures_3(self, aaa_molsys, ala_template):
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        topo = molsys_no_cb.topology
        coords = puw.get_value(molsys_no_cb.structures.coordinates, to_unit="nm")
        n_structures = coords.shape[0]
        result = place_missing_in_group(topo, coords, group_idx=0,
                                        missing_names=["CB"], template=ala_template)
        assert result["CB"].shape == (n_structures, 3)

    def test_no_common_atoms_returns_empty(self, ala_template):
        """If no atoms in the group match the template, nothing can be placed."""
        from molsysmt.native.topology import Atoms_DataFrame
        atoms = Atoms_DataFrame(n_atoms=1)
        atoms.loc[0, "atom_name"] = "UNKNOWN"
        atoms.loc[0, "group_index"] = 0
        # Build a minimal topology-like object
        class MinTopo:
            pass
        topo = MinTopo()
        topo.atoms = atoms
        coords = np.zeros((1, 1, 3), dtype=np.float64)
        result = place_missing_in_group(topo, coords, group_idx=0,
                                        missing_names=["CB"], template=ala_template)
        assert result == {}

    def test_placed_cb_is_near_ca(self, aaa_molsys, ala_template):
        """Placed CB should be within a reasonable bond distance of CA (~0.15 nm)."""
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        molsys_no_cb = msm.remove(aaa_molsys, selection='atom_name=="CB"')
        topo = molsys_no_cb.topology
        coords = puw.get_value(molsys_no_cb.structures.coordinates, to_unit="nm")
        result = place_missing_in_group(topo, coords, group_idx=0,
                                        missing_names=["CB"], template=ala_template)
        ca_idx = topo.atoms[(topo.atoms["group_index"] == 0) &
                            (topo.atoms["atom_name"] == "CA")].index[0]
        ca_pos = coords[0, ca_idx, :]
        cb_pos = result["CB"][0]
        dist = np.linalg.norm(cb_pos - ca_pos)
        assert 0.10 < dist < 0.20, f"CA-CB distance {dist:.3f} nm out of range"


# ---------------------------------------------------------------------------
# append_atoms_to_molsys
# ---------------------------------------------------------------------------

class TestAppendAtomsToMolsys:

    def test_atom_count_increases(self, aaa_molsys):
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        n_orig = aaa_molsys.topology.n_atoms
        coords_dummy = np.zeros((1, 3), dtype=np.float64)
        new_atom_info = [(0, "XX", coords_dummy)]   # group 0, fake atom
        result = append_atoms_to_molsys(aaa_molsys, new_atom_info, [])
        assert result.topology.n_atoms == n_orig + 1

    def test_new_atom_has_correct_group_index(self, aaa_molsys):
        coords_dummy = np.zeros((1, 3), dtype=np.float64)
        new_atom_info = [(1, "XX", coords_dummy)]   # group 1
        result = append_atoms_to_molsys(aaa_molsys, new_atom_info, [])
        xx_rows = result.topology.atoms[result.topology.atoms["atom_name"] == "XX"]
        assert len(xx_rows) == 1
        assert int(xx_rows.iloc[0]["group_index"]) == 1

    def test_bond_is_added(self, aaa_molsys):
        n_bonds_orig = aaa_molsys.topology.bonds.shape[0]
        n_orig = aaa_molsys.topology.n_atoms
        coords_dummy = np.zeros((1, 3), dtype=np.float64)
        new_atom_info = [(0, "XX", coords_dummy)]
        new_bonds_info = [(0, n_orig)]   # bond from atom 0 to new atom
        result = append_atoms_to_molsys(aaa_molsys, new_atom_info, new_bonds_info)
        assert result.topology.bonds.shape[0] == n_bonds_orig + 1

    def test_coordinates_shape_is_correct(self, aaa_molsys):
        from molsysmt import pyunitwizard as puw
        n_structures = aaa_molsys.structures.n_structures
        coords_dummy = np.zeros((n_structures, 3), dtype=np.float64)
        new_atom_info = [(0, "XX", coords_dummy)]
        result = append_atoms_to_molsys(aaa_molsys, new_atom_info, [])
        out_coords = puw.get_value(result.structures.coordinates, to_unit="nm")
        assert out_coords.shape == (n_structures, aaa_molsys.topology.n_atoms + 1, 3)

    def test_no_new_atoms_returns_equivalent(self, aaa_molsys):
        result = append_atoms_to_molsys(aaa_molsys, [], [])
        assert result.topology.n_atoms == aaa_molsys.topology.n_atoms


# ---------------------------------------------------------------------------
# place_ace_group
# ---------------------------------------------------------------------------

class TestPlaceAceGroup:

    def _make_positions(self):
        """Simple backbone N, CA, C positions for one structure."""
        N  = np.array([[0.000, 0.000, 0.000]])
        CA = np.array([[0.146, 0.000, 0.000]])
        C  = np.array([[0.146, 0.146, 0.000]])
        return N, CA, C

    def test_returns_all_ace_atoms(self, ace_template):
        N, CA, C = self._make_positions()
        result = place_ace_group(N, CA, C, ace_template, n_structures=1)
        for atom in ace_template["atoms"]:
            assert atom in result, f"ACE atom {atom!r} missing from result"

    def test_output_shape(self, ace_template):
        N, CA, C = self._make_positions()
        result = place_ace_group(N, CA, C, ace_template, n_structures=1)
        for atom, coords in result.items():
            assert coords.shape == (1, 3), f"{atom} has wrong shape {coords.shape}"

    def test_c_ace_distance_from_n(self, ace_template):
        """C(ACE) must be ~0.133 nm from N (peptide bond length)."""
        N, CA, C = self._make_positions()
        result = place_ace_group(N, CA, C, ace_template, n_structures=1)
        dist = np.linalg.norm(result["C"][0] - N[0])
        assert 0.12 < dist < 0.15, f"C(ACE)–N distance {dist:.3f} nm out of range"

    def test_multiple_structures(self, ace_template):
        n = 5
        N  = np.tile([0.000, 0.000, 0.000], (n, 1))
        CA = np.tile([0.146, 0.000, 0.000], (n, 1))
        C  = np.tile([0.146, 0.146, 0.000], (n, 1))
        result = place_ace_group(N, CA, C, ace_template, n_structures=n)
        for atom, coords in result.items():
            assert coords.shape == (n, 3)


# ---------------------------------------------------------------------------
# place_nme_group
# ---------------------------------------------------------------------------

class TestPlaceNmeGroup:

    def _make_positions(self):
        """Simple backbone C, CA, N positions for one structure."""
        C  = np.array([[0.000, 0.000, 0.000]])
        CA = np.array([[-0.146, 0.000, 0.000]])
        N  = np.array([[0.000, 0.146, 0.000]])
        return C, CA, N

    def test_returns_all_nme_atoms(self, nme_template):
        C, CA, N = self._make_positions()
        result = place_nme_group(C, CA, N, nme_template, n_structures=1)
        for atom in nme_template["atoms"]:
            assert atom in result, f"NME atom {atom!r} missing from result"

    def test_output_shape(self, nme_template):
        C, CA, N = self._make_positions()
        result = place_nme_group(C, CA, N, nme_template, n_structures=1)
        for atom, coords in result.items():
            assert coords.shape == (1, 3)

    def test_n_nme_distance_from_c(self, nme_template):
        """N(NME) must be ~0.133 nm from C (peptide bond length)."""
        C, CA, N = self._make_positions()
        result = place_nme_group(C, CA, N, nme_template, n_structures=1)
        dist = np.linalg.norm(result["N"][0] - C[0])
        assert 0.12 < dist < 0.15, f"N(NME)–C distance {dist:.3f} nm out of range"

    def test_multiple_structures(self, nme_template):
        n = 5
        C  = np.tile([0.000, 0.000, 0.000], (n, 1))
        CA = np.tile([-0.146, 0.000, 0.000], (n, 1))
        N  = np.tile([0.000, 0.146, 0.000], (n, 1))
        result = place_nme_group(C, CA, N, nme_template, n_structures=n)
        for atom, coords in result.items():
            assert coords.shape == (n, 3)


# ---------------------------------------------------------------------------
# rebuild_molsys_with_new_groups
# ---------------------------------------------------------------------------

class TestRebuildMolsysWithNewGroups:

    def test_ace_inserted_as_first_group(self, aaa_molsys, ace_template):
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        topo = aaa_molsys.topology
        coords = puw.get_value(aaa_molsys.structures.coordinates, to_unit="nm")
        n_structures = coords.shape[0]

        # ACE placed at trivial position (zeros) — we test structure, not geometry
        ace_atoms = {a: np.zeros((n_structures, 3)) for a in ace_template["atoms"]}
        mol_group_ranges = {0: (0, 2)}
        extra_before = {0: ("ACE", ace_atoms)}

        result = rebuild_molsys_with_new_groups(
            aaa_molsys, mol_group_ranges, extra_before, {}
        )
        group_names = msm.get(result, element="group", group_name=True)
        assert group_names[0] == "ACE"
        assert group_names[1:] == ["ALA", "ALA", "ALA"]

    def test_nme_appended_as_last_group(self, aaa_molsys, nme_template):
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        coords = puw.get_value(aaa_molsys.structures.coordinates, to_unit="nm")
        n_structures = coords.shape[0]

        nme_atoms = {a: np.zeros((n_structures, 3)) for a in nme_template["atoms"]}
        mol_group_ranges = {0: (0, 2)}
        extra_after = {0: ("NME", nme_atoms)}

        result = rebuild_molsys_with_new_groups(
            aaa_molsys, mol_group_ranges, {}, extra_after
        )
        group_names = msm.get(result, element="group", group_name=True)
        assert group_names[-1] == "NME"
        assert group_names[:-1] == ["ALA", "ALA", "ALA"]

    def test_no_insertions_preserves_system(self, aaa_molsys):
        import molsysmt as msm
        n_atoms_before = msm.get(aaa_molsys, n_atoms=True)
        result = rebuild_molsys_with_new_groups(aaa_molsys, {}, {}, {})
        assert msm.get(result, n_atoms=True) == n_atoms_before

    def test_existing_bonds_are_remapped(self, aaa_molsys, ace_template):
        import molsysmt as msm
        from molsysmt import pyunitwizard as puw
        coords = puw.get_value(aaa_molsys.structures.coordinates, to_unit="nm")
        n_structures = coords.shape[0]
        n_bonds_orig = aaa_molsys.topology.bonds.shape[0]

        ace_atoms = {a: np.zeros((n_structures, 3)) for a in ace_template["atoms"]}
        mol_group_ranges = {0: (0, 2)}

        result = rebuild_molsys_with_new_groups(
            aaa_molsys, mol_group_ranges, {0: ("ACE", ace_atoms)}, {}
        )
        # Original bonds must be preserved (remapped) + ACE intra-group + ACE–ALA peptide bond
        n_bonds_result = result.topology.bonds.shape[0]
        assert n_bonds_result > n_bonds_orig
