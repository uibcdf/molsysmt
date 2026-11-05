"""Solvate actual systems with nullable labels; never use labels as indices."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError

puw = msm.pyunitwizard


@pytest.fixture(scope="module")
def solute():
    pytest.importorskip("openmm")
    return msm.build.add_missing_terminal_cappings(msm.build.build_peptide("AlaValPro"))


def identifiers(kind, size):
    if kind == "numeric":
        return [str(i + 1) for i in range(size)]
    if kind == "nonconsecutive":
        return [str(100 * (i + 1)) for i in range(size)]
    if kind == "arbitrary":
        return [f"alpha-{i}" for i in range(size)]
    if kind == "missing":
        return [None] * size
    if kind == "duplicates":
        return ["42"] * size
    values = [f"label-{i}" for i in range(size)]
    values[: min(size, 6)] = ["<NA>", None, "None", "nan", "", "1"][: min(size, 6)]
    return values


@pytest.mark.parametrize(
    "kind",
    [
        "numeric",
        "nonconsecutive",
        "arbitrary",
        "missing",
        "duplicates",
        "literal_sentinels",
    ],
)
@pytest.mark.parametrize("native_ions", [False, True])
def test_source_atom_and_group_ids_are_preserved(solute, kind, native_ions):
    source = solute.copy()
    natoms, ngroups = source.topology.n_atoms, source.topology.n_groups
    atom_ids, group_ids = identifiers(kind, natoms), identifiers(kind, ngroups)
    msm.set(source, element="atom", atom_id=atom_ids)
    msm.set(source, element="group", group_id=group_ids)
    original_atoms = source.topology.atoms.copy(deep=True)
    original_groups = source.topology.groups.copy(deep=True)
    original_xyz = puw.get_value(source.structures.coordinates).copy()
    kwargs = dict(n_cations=1, n_anions=1, random_seed=5) if native_ions else {}
    output = msm.build.solvate(
        source, engine="OpenMM", box_shape="cubic", clearance="0.6 nm", **kwargs
    )
    assert msm.get(output, n_waters=True) > 0
    assert (
        msm.get(output, element="atom", selection=np.arange(natoms), atom_id=True)
        == atom_ids
    )
    assert (
        msm.get(output, element="group", selection=np.arange(ngroups), group_id=True)
        == group_ids
    )
    assert (
        output.topology.atoms.atom_name.iloc[:natoms].tolist()
        == source.topology.atoms.atom_name.tolist()
    )
    for original, result in [
        (atom_ids, output.topology.atoms.atom_id.iloc[natoms:]),
        (group_ids, output.topology.groups.group_id.iloc[ngroups:]),
    ]:
        reserved = {label for label in original if label is not None}
        generated = result.tolist()
        assert len(generated) == len(set(generated))
        assert set(generated).isdisjoint(reserved)
        assert all(isinstance(label, str) and label.isdecimal() for label in generated)
        expected = []
        candidate = 1
        while len(expected) < len(generated):
            if str(candidate) not in reserved:
                expected.append(str(candidate))
            candidate += 1
        assert generated == expected
    # Solvation may translate the source rigidly; atom correspondence and
    # all relative coordinates must remain intact.
    shifted = puw.get_value(output.structures.coordinates)[0, :natoms] - original_xyz[0]
    np.testing.assert_allclose(
        shifted, np.broadcast_to(shifted[0], shifted.shape), atol=1e-12
    )
    before_bonds = source.chemical_states._states[0].bonds
    after_bonds = output.chemical_states._states[0].bonds
    retained = after_bonds[
        (after_bonds.atom1_index < natoms) & (after_bonds.atom2_index < natoms)
    ]
    assert set(map(tuple, retained[["atom1_index", "atom2_index"]].to_numpy())) == set(
        map(tuple, before_bonds[["atom1_index", "atom2_index"]].to_numpy())
    )
    pd.testing.assert_frame_equal(source.topology.atoms, original_atoms)
    pd.testing.assert_frame_equal(source.topology.groups, original_groups)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates), original_xyz
    )


def test_bundled_missing_ids_no_longer_prevent_solvation():
    pytest.importorskip("openmm")
    source = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        to_form="molsysmt.MolSys",
        structure_indices=0,
    )
    # The legacy reader already represents these labels as literal 'None'.
    # Do not reinterpret that spelling as a missing value during preparation.
    expected = source.topology.atoms.atom_id.tolist()
    assert set(expected) == {"None"}
    output = msm.build.solvate(
        source, engine="OpenMM", box_shape="cubic", clearance="0.35 nm"
    )
    assert (
        output.topology.atoms.atom_id.iloc[: source.topology.n_atoms].tolist()
        == expected
    )
    assert msm.get(output, n_waters=True) > 0


def test_h5msm_preserves_missing_and_literal_ids(solute, tmp_path):
    source = solute.copy()
    msm.set(source, selection=[0, 1, 2], atom_id=[None, "<NA>", "alpha"])
    path = str(tmp_path / "solvated.h5msm")
    returned = msm.build.solvate(
        source, engine="OpenMM", box_shape="cubic", clearance="0.35 nm", to_form=path
    )
    assert returned == path
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert msm.get(restored, element="atom", selection=[0, 1, 2], atom_id=True) == [
        None,
        "<NA>",
        "alpha",
    ]


def test_foreign_input_and_output_keep_present_labels(solute):
    source = msm.convert(solute, to_form="openmm.Modeller")
    atoms, groups = list(source.topology.atoms()), list(source.topology.residues())
    atoms[0].id, groups[0].id = "atom-alpha", "group-beta"
    original_positions = puw.get_value(
        puw.convert(source.positions, to_form="pint"), to_unit="nm"
    ).copy()
    output = msm.build.solvate(
        source, engine="OpenMM", box_shape="cubic", clearance="0.35 nm"
    )
    assert msm.get_form(output) == "openmm.Modeller"
    assert list(output.topology.atoms())[0].id == "atom-alpha"
    assert list(output.topology.residues())[0].id == "group-beta"
    assert atoms[0].id == "atom-alpha" and groups[0].id == "group-beta"
    assert source.topology.getNumAtoms() == solute.topology.n_atoms
    np.testing.assert_array_equal(
        puw.get_value(puw.convert(source.positions, to_form="pint"), to_unit="nm"),
        original_positions,
    )


def test_original_water_replacement_uses_ion_map_instead_of_prefix():
    source = msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"))
    source = msm.extract(source, selection=[0, 1, 2])
    msm.set(source, element="atom", atom_id=["source-O", "source-H1", "source-H2"])
    msm.set(source, element="group", group_id=["source-water"])
    water_only = msm.build.solvate(
        source,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.6 nm",
        n_cations=0,
        n_anions=0,
        random_seed=0,
    )
    n_waters = msm.get(water_only, n_waters=True)
    seed = next(
        seed
        for seed in range(10000)
        if np.random.Generator(np.random.PCG64(seed)).permutation(n_waters)[0] == 0
    )
    output = msm.build.solvate(
        source,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.6 nm",
        n_cations=1,
        n_anions=0,
        random_seed=seed,
    )
    report = output.chemical_states._states[0]._preparation_history[-1]["report"]
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"][:3], [-1, -1, -1]
    )
    assert set(source.topology.atoms.atom_id).isdisjoint(
        set(output.topology.atoms.atom_id)
    )
    assert "source-water" not in output.topology.groups.group_id.tolist()
    assert report["solvation"]["n_source_atoms"] == 3
    assert msm.get(source, n_atoms=True, n_waters=True) == [3, 1]


def test_noncanonical_provider_indices_are_rejected_before_solvent(solute, monkeypatch):
    from openmm.app import Modeller

    source = msm.convert(solute, to_form="openmm.Modeller")
    atom = list(source.topology.atoms())[0]
    atom.index = 9

    def forbidden(*args, **kwargs):
        raise AssertionError("Invalid source traversal reached solvent construction")

    monkeypatch.setattr(Modeller, "addSolvent", forbidden)
    with pytest.raises(StructuralInconsistencyError, match="traversal"):
        msm.build.solvate(
            source, engine="OpenMM", box_shape="cubic", clearance="0.35 nm"
        )
