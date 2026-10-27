"""MDTraj-required parents are target-only placeholders with stable atom order."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


def source(smiles="CCO.COC"):
    from rdkit import Chem

    return msm.convert(Chem.MolFromSmiles(smiles), to_form="molsysmt.MolSys")


@pytest.mark.parametrize("form", ["molsysmt.Topology", "molsysmt.MolSys"])
@pytest.mark.parametrize(
    "selection,expected",
    [
        ("index 0", [0]),
        ("index 5 or index 2", [2, 5]),
        ("name O2", [2]),
        ("element O", [2, 4]),
        ("resid 0", [0, 1, 2]),
        ("protein", []),
        ("name ZZZX", []),
    ],
)
def test_group_free_external_selection_preserves_atom_correspondence(
    form, selection, expected
):
    molsys = source()
    item = molsys.topology if form == "molsysmt.Topology" else molsys
    before = molsys.topology.atoms.copy(deep=True)
    groups = molsys.topology.groups.copy(deep=True)
    molecules = molsys.topology.molecules.copy(deep=True)
    assert msm.select(item, selection=selection, syntax="MDTraj") == expected
    pd.testing.assert_frame_equal(before, pd.DataFrame(molsys.topology.atoms))
    pd.testing.assert_frame_equal(groups, pd.DataFrame(molsys.topology.groups))
    pd.testing.assert_frame_equal(molecules, pd.DataFrame(molsys.topology.molecules))
    assert molsys.topology.n_chains == 0


def test_group_free_target_preserves_formal_charges_bonds_and_atom_labels():
    molsys = source("CC[NH3+].CC(=O)[O-]")
    before = deepcopy(molsys.chemical_states._states[0])
    target = msm.convert(molsys, to_form="mdtraj.Topology")
    assert target.n_atoms == 7 and target.n_residues == 2 and target.n_chains == 1
    assert [a.formal_charge for a in target.atoms] == [0, 0, 1, 0, 0, 0, -1]
    assert [a.serial for a in target.atoms] == molsys.topology.atoms.atom_id.tolist()
    assert {tuple(sorted((a.index, b.index))) for a, b in target.bonds} == {
        (0, 1),
        (1, 2),
        (3, 4),
        (4, 5),
        (4, 6),
    }
    assert [r.name for r in target.residues] == ["UNL", "UNL"]
    pd.testing.assert_frame_equal(
        before.atom_attributes, molsys.chemical_states._states[0].atom_attributes
    )
    pd.testing.assert_frame_equal(
        pd.DataFrame(before.bonds),
        pd.DataFrame(molsys.chemical_states._states[0].bonds),
    )


def test_partial_groups_and_chains_keep_declared_rows_and_preserve_missing_source():
    molsys = source()
    top = molsys.topology
    top.reset_groups(n_groups=1)
    top.groups["group_name"] = ["LIG"]
    top.groups["group_id"] = pd.Series(["42"], dtype="string")
    top.groups["molecule_index"] = [0]
    top.atoms["group_index"] = [0, 0, None, None, None, None]
    top.reset_chains(n_chains=2)
    top.chains["chain_id"] = pd.Series(["A", "B"], dtype="string")
    top.atoms["chain_index"] = [None, 1, None, None, None, None]
    before = top.atoms.copy(deep=True)
    target = msm.convert(top, to_form="mdtraj.Topology")
    assert target.n_atoms == 6 and target.n_chains == 3 and target.n_residues == 5
    assert target.residue(0).name == "LIG"
    assert target.residue(0).resSeq == "42"
    assert target.residue(0).chain.index == 1
    assert [a.residue.index for a in target.atoms] == [0, 0, 1, 2, 3, 4]
    assert [c.chain_id for c in list(target.chains)[:2]] == ["A", "B"]
    pd.testing.assert_frame_equal(before, pd.DataFrame(top.atoms))


def test_conflicting_declared_group_chains_raise_clear_error():
    molsys = source("CCO")
    top = molsys.topology
    top.reset_groups(n_groups=1)
    top.groups["group_name"] = ["LIG"]
    top.groups["molecule_index"] = [0]
    top.atoms["group_index"] = [0, 0, 0]
    top.reset_chains(n_chains=2)
    top.atoms["chain_index"] = [0, 1, 1]
    with pytest.raises(msm.StructuralInconsistencyError, match="multiple chains"):
        msm.convert(top, to_form="mdtraj.Topology")
    assert top.atoms.chain_index.tolist() == [0, 1, 1]


@pytest.mark.parametrize("selection", [[], [2, 1, 0], [5, 0]])
def test_atom_subset_follows_native_extraction_order_and_empty_output(selection):
    molsys = source()
    target = msm.convert(molsys, to_form="mdtraj.Topology", selection=selection)
    assert target.n_atoms == len(selection)
    assert [a.serial for a in target.atoms] == [str(i) for i in sorted(selection)]
    if selection == [2, 1, 0]:
        assert [a.element.symbol for a in target.atoms] == ["C", "C", "O"]
        assert [a.name for a in target.atoms] == ["C0", "C1", "O2"]
        assert {tuple(sorted((a.index, b.index))) for a, b in target.bonds} == {
            (0, 1),
            (1, 2),
        }
    elif selection:
        assert [a.name for a in target.atoms] == ["C0", "C5"]
        assert target.n_bonds == 0
    else:
        assert target.n_residues == 0 and target.n_chains == 0


def test_external_selector_is_usable_by_complete_molecule_descriptors():
    molsys = source()
    result = msm.physchem.get_tpsa(
        molsys, selection="index 0", syntax="MDTraj", return_report=True
    )
    assert result["report"]["molecule_indices"].tolist() == [0]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["tpsa"], to_unit="angstrom**2"),
        [20.23],
        atol=1e-12,
    )
    assert molsys.topology.n_groups == 0


def test_explicitly_permuted_source_retains_atom_order_in_the_target():
    molsys = msm.permute_atoms(source(), atom_indices=[2, 1, 0, 5, 4, 3])
    target = msm.convert(molsys, to_form="mdtraj.Topology")
    assert [a.name for a in target.atoms] == ["O2", "C1", "C0", "C5", "O4", "C3"]
    assert [a.serial for a in target.atoms] == ["2", "1", "0", "5", "4", "3"]
    assert msm.select(molsys, selection="index 0", syntax="MDTraj") == [0]
