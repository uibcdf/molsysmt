"""Preserving explicit chain labels independently of appended chain indices."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


@pytest.mark.parametrize("in_place", [False, True])
def test_add_preserves_duplicate_chain_ids_and_names(alanine_molsys, in_place):
    target = alanine_molsys
    source = target.copy()
    msm.set(target, element="chain", chain_id=["A"], chain_name=["target"])
    msm.set(source, element="chain", chain_id=["A"], chain_name=["source"])
    source_chains = source.topology.chains.copy(deep=True)
    n_target = target.topology.n_atoms
    n_source = source.topology.n_atoms

    result = msm.add(
        target, source, keep_ids=True, in_place=in_place, attribute_policy="strict"
    )
    combined = target if in_place else result

    assert msm.get(combined, element="chain", chain_id=True) == ["A", "A"]
    assert msm.get(combined, element="chain", chain_name=True) == ["target", "source"]
    np.testing.assert_array_equal(
        combined.topology.atoms["chain_index"], [0] * n_target + [1] * n_source
    )
    pd.testing.assert_frame_equal(source.topology.chains, source_chains)
    if not in_place:
        assert msm.get(target, element="chain", chain_id=True) == ["A"]
        assert target.topology.n_atoms == n_target


def test_selected_source_keeps_its_chain_label_after_index_remapping(alanine_molsys):
    source = msm.merge([alanine_molsys, alanine_molsys, alanine_molsys])
    msm.set(
        source,
        element="chain",
        chain_id=["X", "Y", "Z"],
        chain_name=["one", "two", "three"],
    )
    msm.set(alanine_molsys, element="chain", chain_id=["A"])
    n_atoms = alanine_molsys.topology.n_atoms
    selected = [2 * n_atoms + 1, 2 * n_atoms]

    combined = msm.add(
        alanine_molsys, source, selection=selected, in_place=False, keep_ids=True
    )

    assert msm.get(combined, element="chain", chain_id=True) == ["A", "Z"]
    assert msm.get(combined, element="chain", chain_name=True)[1] == "three"
    assert combined.topology.atoms["chain_index"].iloc[-2:].tolist() == [1, 1]
    assert msm.get(source, element="chain", chain_id=True) == ["X", "Y", "Z"]


def test_native_topology_add_keeps_labels_and_can_explicitly_regenerate_them(
    alanine_molsys,
):
    target = alanine_molsys.topology.copy()
    source = target.copy()
    target.chains["chain_id"] = pd.array(["A"], dtype="string")
    source.chains["chain_id"] = pd.array(["A"], dtype="string")

    target.add(source, keep_ids=True, skip_digestion=True)
    assert target.chains["chain_id"].tolist() == ["A", "A"]
    assert str(target.chains["chain_id"].dtype) == "string"

    target.add(source, keep_ids=False, skip_digestion=True)
    assert target.chains["chain_id"].tolist() == ["0", "1", "2"]
    assert source.chains["chain_id"].tolist() == ["A"]


def test_pdbqt_writer_retains_duplicate_declared_chain_ids(alanine_molsys, tmp_path):
    from molsysmt.form.molsysmt_MolSys.to_file_pdbqt import to_file_pdbqt

    molsys = msm.extract(alanine_molsys, selection=[0, 1])
    msm.set(molsys, element="chain", chain_id=["A"])
    molsys.molecular_mechanics.partial_charge = np.array([0.2, -0.2])
    molsys.molecular_mechanics.atom_ff_type = molsys.topology.atoms[
        "atom_type"
    ].to_numpy(dtype=str)
    source = molsys.copy()
    msm.set(molsys, element="atom", atom_id=[1, 2])
    msm.set(source, element="atom", atom_id=[3, 4])
    combined = msm.add(
        molsys, source, in_place=False, keep_ids=True, attribute_policy="strict"
    )

    output = tmp_path / "chains.pdbqt"
    to_file_pdbqt(
        combined,
        output_filename=str(output),
        typing_scheme="autodock4",
        torsion_tree=None,
    )
    records = [
        line
        for line in output.read_text().splitlines()
        if line.startswith(("ATOM  ", "HETATM"))
    ]
    assert len(records) == 4
    assert [line[21] for line in records] == ["A"] * 4
