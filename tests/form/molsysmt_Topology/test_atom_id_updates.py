"""Preserving string atom labels through public and native adapter edits."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form.molsysmt_Topology.set import set_atom_id_to_atom


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("label", [101, np.int64(101), "101", "00101", "CA_label"])
def test_public_scalar_atom_id_roundtrip(form, label, hp35_pdb_molsys):
    source = msm.convert(hp35_pdb_molsys, to_form=form)
    before = msm.get(source, element="atom", atom_id=True).copy()
    msm.set(source, selection=[1], atom_id=label)
    after = msm.get(source, element="atom", atom_id=True)
    assert after[1] == str(label)
    assert isinstance(after[1], str)
    assert [after[0], after[2]] == [before[0], before[2]]
    assert msm.get(source, element="atom", selection=[1], atom_index=True) == [1]


@pytest.mark.parametrize("all_atoms", [False, True])
def test_public_numeric_atom_id_vectors_preserve_string_storage(
    all_atoms, hp35_pdb_molsys
):
    source = msm.copy(hp35_pdb_molsys)
    indices = list(range(msm.get(source, n_atoms=True))) if all_atoms else [0, 2]
    labels = np.arange(len(indices)) + 1000
    before = msm.get(source, element="atom", atom_id=True).copy()
    msm.set(source, selection="all" if all_atoms else indices, atom_id=labels)
    after = msm.get(source, element="atom", atom_id=True)
    assert all(isinstance(label, str) for label in after)
    assert [after[index] for index in indices] == [str(label) for label in labels]
    if not all_atoms:
        assert after[1] == before[1]


@pytest.mark.parametrize("label", [101, "00101"])
@pytest.mark.parametrize("all_atoms", [False, True])
def test_scalar_atom_label_broadcasts_to_selected_atoms(
    label, all_atoms, hp35_pdb_molsys
):
    source = msm.copy(hp35_pdb_molsys)
    before = msm.get(source, element="atom", atom_id=True).copy()
    msm.set(source, selection="all" if all_atoms else [2, 0], atom_id=label)
    assert (
        msm.get(source, element="atom", selection=[2, 0], atom_id=True)
        == [str(label)] * 2
    )
    if all_atoms:
        assert msm.get(source, element="atom", atom_id=True) == [str(label)] * len(
            before
        )
    else:
        assert (
            msm.get(source, element="atom", selection=[1], atom_id=True)[0] == before[1]
        )


def test_trusted_native_adapter_keeps_numeric_atom_ids_as_strings(hp35_pdb_molsys):
    topology = hp35_pdb_molsys.topology.copy()
    set_atom_id_to_atom(topology, indices=[1], value=101, skip_digestion=True)
    assert msm.get(topology, element="atom", selection=[1], atom_id=True) == ["101"]


def test_edited_atom_labels_survive_public_h5msm_roundtrip(hp35_pdb_molsys, tmp_path):
    source = msm.copy(hp35_pdb_molsys)
    msm.set(source, selection=[2, 0], atom_id=["00101", "custom_label"])
    path = str(tmp_path / "labels.h5msm")
    msm.convert(source, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    np.testing.assert_array_equal(
        msm.get(restored, element="atom", atom_id=True),
        msm.get(source, element="atom", atom_id=True),
    )
