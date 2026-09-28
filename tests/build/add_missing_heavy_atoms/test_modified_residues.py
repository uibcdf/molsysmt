"""Chemical and geometric regression tests for curated modified residues."""

from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.residue_templates import load_residue_template
from molsysmt._private.smonitor import UnassessedResidueWarning

SOURCE_ROOT = Path(__file__).resolve().parents[3] / "molsysmt" / "data" / "pdb"
CASES = [
    ("MSE", "3c8h.pdb", "A", 27, "O", "O"),
    ("SEP", "1atp.pdb", "E", 338, "O1P", "O"),
]


def _observed_residue(filename, group_name, chain_id, group_id):
    """Read one complete, bundled experimental residue as an independent reference."""

    observed = {}
    for line in (SOURCE_ROOT / filename).read_text().splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        if (
            line[17:20] != group_name
            or line[21] != chain_id
            or line[22:26].strip() != str(group_id)
            or line[16] not in {" ", "A"}
        ):
            continue
        atom_name = line[12:16].strip()
        element = line[76:78].strip().capitalize()
        coords_nm = np.array(
            [float(line[start : start + 8]) / 10 for start in (30, 38, 46)]
        )
        observed[atom_name] = (element, coords_nm)
    return observed


def _ideal_residue(group_name):
    template = load_residue_template(group_name)
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    return {
        name: (element, np.asarray(coords) @ rotation + np.array([2.0, 3.0, 4.0]))
        for name, element, coords in zip(
            template["atoms"], template["elements"], template["coords_nm"]
        )
    }


def _incomplete_residue(case, missing_names, *, ideal=False):
    """Build a small residue with observed geometry and curated connectivity."""

    group_name, filename, chain_id, group_id, _, _ = case
    observed = (
        _ideal_residue(group_name)
        if ideal
        else _observed_residue(filename, group_name, chain_id, group_id)
    )
    template = load_residue_template(group_name)
    builder = msm.MolSysBuilder()
    indices = {}
    for name, (element, _) in observed.items():
        if name not in missing_names:
            indices[name] = builder.add_atom(
                atom_id=str(100 + len(indices)), atom_name=name, atom_type=element
            )
    builder.add_group(
        list(indices.values()), group_id=str(group_id), group_name=group_name
    )
    for (name1, name2), order in zip(template["bonds"], template["bond_orders"]):
        if name1 in indices and name2 in indices:
            builder.add_bond(
                indices[name1], indices[name2], bond_order=order, bond_type="covalent"
            )
    coords = np.array([observed[name][1] for name in indices])
    builder.set_coordinates(puw.quantity(coords, "nm"))
    return builder.build(), observed


@pytest.mark.parametrize("case", CASES, ids=[case[0] for case in CASES])
def test_repair_matches_observed_modified_residue_chemistry_and_geometry(case):
    group_name, _, _, _, missing_name, expected_element = case
    molsys, observed = _incomplete_residue(
        case, {missing_name}, ideal=group_name == "SEP"
    )
    original_atoms = molsys.topology.atoms.copy()
    original_coords = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()

    assert msm.build.get_missing_heavy_atoms(molsys) == {0: [missing_name]}
    repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")

    atoms = repaired.topology.atoms
    assert repaired.topology.groups.loc[0, "group_name"] == group_name
    assert repaired.topology.groups.loc[0, "group_id"] == str(case[3])
    assert set(atoms["atom_name"]) == set(observed)
    assert len(set(atoms["atom_id"])) == len(atoms)
    assert (
        atoms.loc[atoms["atom_name"] == missing_name, "atom_type"].iloc[0]
        == expected_element
    )

    new_coords = puw.get_value(repaired.structures.coordinates, to_unit="nm")
    assert new_coords.shape == (1, len(observed), 3)
    original_by_name = dict(zip(original_atoms["atom_name"], original_coords[0]))
    repaired_by_name = dict(zip(atoms["atom_name"], new_coords[0]))
    original_ids = dict(zip(original_atoms["atom_name"], original_atoms["atom_id"]))
    repaired_ids = dict(zip(atoms["atom_name"], atoms["atom_id"]))
    for name, coords in original_by_name.items():
        np.testing.assert_array_equal(repaired_by_name[name], coords)
        assert repaired_ids[name] == original_ids[name]
    assert (
        np.linalg.norm(repaired_by_name[missing_name] - observed[missing_name][1])
        < 0.05
    )

    indices = dict(zip(atoms["atom_name"], atoms.index))
    bonds = repaired.topology.bonds
    bonded_names = {
        frozenset((atoms.loc[i1, "atom_name"], atoms.loc[i2, "atom_name"]))
        for i1, i2 in zip(bonds["atom1_index"], bonds["atom2_index"])
    }
    template = load_residue_template(group_name)
    assert bonded_names == {
        frozenset(pair)
        for pair in template["bonds"]
        if all(name in indices for name in pair)
    }
    orders_by_pair = {
        frozenset((atoms.loc[i1, "atom_name"], atoms.loc[i2, "atom_name"])): int(order)
        for i1, i2, order in zip(
            bonds["atom1_index"], bonds["atom2_index"], bonds["bond_order"]
        )
    }
    for pair, order in zip(template["bonds"], template["bond_orders"]):
        if all(name in indices for name in pair):
            assert orders_by_pair[frozenset(pair)] == order


def test_ambiguous_phosphate_oxygen_repair_leaves_sep_unchanged():
    molsys, _ = _incomplete_residue(CASES[1], {"O1P", "O2P"})
    original_names = molsys.topology.atoms["atom_name"].tolist()

    with pytest.warns(UnassessedResidueWarning, match="unassessed"):
        repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")

    assert repaired.topology.atoms["atom_name"].tolist() == original_names


def test_missing_selenium_uses_curated_element_and_bond_order():
    molsys, observed = _incomplete_residue(CASES[0], {"SE"}, ideal=True)
    molsys.topology.atoms.loc[0, "atom_id"] = str(molsys.topology.n_atoms)
    repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")
    atoms = repaired.topology.atoms
    assert atoms.loc[atoms["atom_name"] == "SE", "atom_type"].iloc[0] == "Se"
    coords = puw.get_value(repaired.structures.coordinates, to_unit="nm")[0]
    atom_idx = atoms.index[atoms["atom_name"] == "SE"][0]
    np.testing.assert_allclose(coords[atom_idx], observed["SE"][1], atol=1e-6)
    assert len(set(atoms["atom_id"])) == len(atoms)


def test_element_mismatch_leaves_modified_residue_unassessed():
    molsys, _ = _incomplete_residue(CASES[0], {"O"}, ideal=True)
    se_index = molsys.topology.atoms.index[molsys.topology.atoms["atom_name"] == "SE"][
        0
    ]
    molsys.topology.atoms.loc[se_index, "atom_type"] = "S"
    with pytest.warns(UnassessedResidueWarning, match="element mismatch"):
        repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")
    assert "O" not in repaired.topology.atoms["atom_name"].tolist()


def test_wrong_modified_atom_name_is_explicitly_unassessed():
    molsys, _ = _incomplete_residue(CASES[0], set(), ideal=True)
    se_index = molsys.topology.atoms.index[molsys.topology.atoms["atom_name"] == "SE"][
        0
    ]
    molsys.topology.atoms.loc[se_index, "atom_name"] = "SD"
    with pytest.warns(UnassessedResidueWarning, match="atom names"):
        repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")
    assert (
        repaired.topology.atoms["atom_name"].tolist()
        == molsys.topology.atoms["atom_name"].tolist()
    )


def test_unsupported_modified_residue_is_reported_without_parent_repair():
    builder = msm.MolSysBuilder()
    atom_index = builder.add_atom(atom_id="1", atom_name="N", atom_type="N")
    builder.add_group([atom_index], group_id="1", group_name="TPO")
    builder.set_coordinates(puw.quantity(np.zeros((1, 3)), "nm"))
    molsys = builder.build()
    with pytest.warns(UnassessedResidueWarning, match="no exact curated"):
        repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")
    assert repaired.topology.atoms["atom_name"].tolist() == ["N"]


def test_conflicting_observed_bond_order_leaves_mse_unassessed():
    molsys, _ = _incomplete_residue(CASES[0], {"O"}, ideal=True)
    bonds = molsys.topology.bonds
    names = molsys.topology.atoms["atom_name"]
    ca_c = next(
        index
        for index, row in bonds.iterrows()
        if {names[row.atom1_index], names[row.atom2_index]} == {"CA", "C"}
    )
    molsys.topology._set_chemical_state_bond_attribute(
        "bond_order", 2, bond_indices=[ca_c]
    )
    with pytest.warns(UnassessedResidueWarning, match="bond order"):
        repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")
    assert "O" not in repaired.topology.atoms["atom_name"].tolist()


def test_missing_observed_bond_is_restored_from_exact_template():
    molsys, _ = _incomplete_residue(CASES[0], {"O"}, ideal=True)
    bonds = molsys.topology.bonds.copy()
    names = molsys.topology.atoms["atom_name"]
    remove_index = next(
        index
        for index, row in bonds.iterrows()
        if {names[row.atom1_index], names[row.atom2_index]} == {"CB", "CG"}
    )
    molsys.topology._set_chemical_state_bonds(
        bonds.drop(index=remove_index).reset_index(drop=True)
    )
    repaired = msm.build.add_missing_heavy_atoms(molsys, engine="MolSysMT")
    atoms = repaired.topology.atoms
    bond_names = {
        frozenset(
            (
                atoms.at[row.atom1_index, "atom_name"],
                atoms.at[row.atom2_index, "atom_name"],
            )
        )
        for row in repaired.topology.bonds.itertuples()
    }
    assert frozenset(("CB", "CG")) in bond_names
