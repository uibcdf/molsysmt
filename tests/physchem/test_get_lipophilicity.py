"""State-preserving molecular model scores and detached attribution contracts."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError


def source(smiles):
    from rdkit import Chem

    return Chem.MolFromSmiles(smiles)


@pytest.mark.parametrize(
    "smiles", ["CCO", "CC[NH3+]", "C[N+](=O)[O-]", "[NH3+]CC(=O)[O-]"]
)
@pytest.mark.parametrize(
    "form", ["rdkit.Mol", "molsysmt.MolSys", "molsysmt.Topology", "h5msm", "sdf"]
)
def test_equivalent_forms_preserve_supplied_state_and_provider_score(
    smiles, form, tmp_path
):
    from rdkit import Chem
    from rdkit.Chem import rdMolDescriptors

    original = source(smiles)
    expected = rdMolDescriptors.CalcCrippenDescriptors(
        original, includeHs=True, force=True
    )[0]
    molsys = Chem.Mol(original)
    if form == "sdf":
        path = tmp_path / "declared.sdf"
        lines = Chem.MolToV3KMolBlock(molsys).splitlines()
        in_atoms = False
        for i, line in enumerate(lines):
            if line == "M  V30 BEGIN ATOM":
                in_atoms = True
            elif line == "M  V30 END ATOM":
                in_atoms = False
            elif in_atoms:
                valence = molsys.GetAtomWithIdx(
                    int(line.split()[2]) - 1
                ).GetTotalValence()
                lines[i] += f" VAL={valence if valence else -1}"
        path.write_text("\n".join(lines) + "\n$$$$\n")
        molsys = str(path)
    elif form == "h5msm":
        molsys = msm.convert(molsys, to_form=str(tmp_path / "source.h5msm"))
    elif form != "rdkit.Mol":
        molsys = msm.convert(molsys, to_form=form)
    result = msm.physchem.get_lipophilicity(molsys, return_report=True)
    assert result["lipophilicity"].dtype == np.float64
    assert result["lipophilicity"].shape == (1,)
    np.testing.assert_allclose(result["lipophilicity"], [expected], atol=1e-12, rtol=0)
    report = result["report"]
    assert report["formal_charges"].tolist() == [Chem.GetFormalCharge(original)]
    charged = [a.GetIdx() for a in original.GetAtoms() if a.GetFormalCharge()]
    assert report["charged_atom_indices"].tolist() == charged
    assert report["charged_atom_offsets"].tolist() == [0, len(charged)]
    assert report["value_kind"] == "wildman_crippen_model_score"
    assert report["value_unit"] == "dimensionless"
    assert report["parameters"]["chemical_preparation"] == "none"


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "selection,indices",
    [
        ("all", [0, 1]),
        ([1, 0, 1], [1, 0, 1]),
        ([], []),
        ("atom_index==3", [1]),
        (0, [0]),
    ],
)
def test_dimensionless_output_and_molecule_axis(unit, selection, indices):
    with msm.pyunitwizard.context(standard_units=[unit, "ps", "radians"]):
        result = msm.physchem.get_lipophilicity(
            source("CCO.CC[NH3+]"), selection=selection, return_report=True
        )
    values = result["lipophilicity"]
    assert isinstance(values, np.ndarray)
    assert values.shape == (len(indices),)
    np.testing.assert_allclose(
        values, np.array([-0.0014, -0.7518])[indices], atol=1e-12, rtol=0
    )
    report = result["report"]
    assert report["molecule_indices"].tolist() == indices
    assert report["atom_offsets"].tolist() == list(range(0, 3 * len(indices) + 1, 3))
    expected_atoms = [a for i in indices for a in range(3 * i, 3 * i + 3)]
    assert report["atom_indices"].tolist() == expected_atoms
    expected_charged = [5 for i in indices if i == 1]
    assert report["charged_atom_indices"].tolist() == expected_charged
    np.testing.assert_array_equal(
        np.diff(report["charged_atom_offsets"]), [int(i == 1) for i in indices]
    )
    for key in (
        "molecule_indices",
        "atom_indices",
        "charged_atom_indices",
        "charged_atom_offsets",
    ):
        assert report[key].dtype == np.int64


@pytest.mark.parametrize(
    "smiles", ["CCO", "c1ccncc1", "[NH3+]CC(=O)[O-]", "C[N+](=O)[O-]"]
)
def test_hydrogen_presentations_and_stale_caches_preserve_source(smiles):
    from rdkit import Chem

    molsys = source(smiles)
    molsys.SetDoubleProp("_crippenLogP", 9999)
    molsys.SetDoubleProp("_crippenMR", 9999)
    before = molsys.ToBinary()
    result = msm.physchem.get_lipophilicity(molsys)
    explicit = msm.physchem.get_lipophilicity(Chem.AddHs(molsys))
    assert molsys.ToBinary() == before
    assert molsys.GetDoubleProp("_crippenLogP") == 9999
    np.testing.assert_allclose(result, explicit, atol=1e-12, rtol=0)
    assert result[0] != 9999


def test_explicit_chemical_states_change_scores_without_preparation():
    molsys = msm.convert(source("CC(=O)O"), to_form="molsysmt.MolSys")
    state = deepcopy(molsys.chemical_states._states[0])
    state.state_id = "acetate"
    state.atom_attributes.loc[3, "formal_charge"] = -1
    state.atom_attributes.loc[3, "n_implicit_hydrogens"] = 0
    molsys.chemical_states._append_state(state, False)
    baseline = molsys.chemical_states._states[0].atom_attributes.copy(deep=True)
    reference = msm.physchem.get_lipophilicity(molsys, return_report=True)
    alternate = msm.physchem.get_lipophilicity(
        molsys, chemical_state=1, return_report=True
    )
    np.testing.assert_allclose(reference["lipophilicity"], [0.0909], atol=1e-12, rtol=0)
    np.testing.assert_allclose(
        alternate["lipophilicity"], [-1.2438], atol=1e-12, rtol=0
    )
    assert alternate["report"]["chemical_state_index"] == 1
    assert alternate["report"]["chemical_state_id"] == "acetate"
    assert (
        alternate["report"]["chemical_graph_digest"]
        != reference["report"]["chemical_graph_digest"]
    )
    pd.testing.assert_frame_equal(
        baseline, molsys.chemical_states._states[0].atom_attributes
    )


@pytest.mark.parametrize(
    "field",
    [
        "formal_charge",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
    ],
)
def test_missing_evidence_is_not_guessed(field):
    molsys = msm.convert(source("CCO"), to_form="molsysmt.MolSys")
    molsys.chemical_states._states[0].atom_attributes[field] = None
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_lipophilicity(molsys)


@pytest.mark.parametrize("smiles", ["[Na+]", "[CH3]", "[*]"])
def test_unsupported_graphs_fail(smiles):
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_lipophilicity(source(smiles))


@pytest.mark.parametrize(
    "name,value",
    [
        ("element", "bond"),
        ("method", "rdkit"),
        ("return_report", "yes"),
        ("skip_digestion", "yes"),
    ],
)
def test_public_validation(name, value):
    with pytest.raises((msm.ArgumentError, ArgumentChoiceError)):
        msm.physchem.get_lipophilicity(source("CCO"), **{name: value})


@pytest.mark.parametrize("bonded", [False, True])
def test_disconnected_salt_label_and_crossed_boundary_fail(bonded):
    from molsysmt.native.topology import Groups_DataFrame

    molsys = msm.convert(source("CC[NH3+].[Cl-]"), to_form="molsysmt.MolSys")
    molsys.topology.groups = Groups_DataFrame(n_groups=2)
    molsys.topology.groups["group_name"] = ["LIG", "ION"]
    molsys.topology.groups["molecule_index"] = [0, 1] if bonded else [0, 0]
    molsys.topology.atoms["group_index"] = [0, 0, 0, 1]
    molsys.topology.reset_molecules(n_molecules=2 if bonded else 1)
    molsys.topology._molecules_dirty = False
    if bonded:
        molsys.topology._append_chemical_state_bonds(
            [[0, 3]], bond_order=[1], bond_type=["covalent"]
        )
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_lipophilicity(molsys, selection=[0])


def test_unselected_unsupported_molecule_is_not_calculated():
    result = msm.physchem.get_lipophilicity(source("CCO.[Zn+2]"), selection=[0])
    np.testing.assert_allclose(result, [-0.0014], atol=1e-12, rtol=0)


def test_no_coordinate_copy_and_structure_associated_state_resolution(monkeypatch):
    molsys = msm.convert(source("CCO"), to_form="molsysmt.MolSys")
    molsys.structures.coordinates = msm.pyunitwizard.quantity(
        np.zeros((20, 3, 3)), "nm"
    )
    state = deepcopy(molsys.chemical_states._states[0])
    state.state_id = "other"
    molsys.chemical_states._append_state(state, False)
    molsys._set_structure_chemical_state_indices([0, 1] + [0] * 18)

    def forbidden(*args, **kwargs):
        raise AssertionError("A graph descriptor must not copy the source structures.")

    monkeypatch.setattr(molsys.structures, "copy", forbidden)
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_lipophilicity(
            molsys, chemical_state="structure", structure_indices=[1, 0]
        )
    result = msm.physchem.get_lipophilicity(
        molsys, chemical_state="structure", structure_indices=[1], return_report=True
    )
    assert result["report"]["chemical_state_index"] == 1
    assert result["lipophilicity"].shape == (1,)


def test_h5msm_bytes_and_source_maps_are_preserved(tmp_path):
    import hashlib
    from pathlib import Path

    path = msm.convert(source("C[N+](=O)[O-]"), to_form=str(tmp_path / "source.h5msm"))
    before = hashlib.sha256(Path(path).read_bytes()).digest()
    first = msm.physchem.get_lipophilicity(path, return_report=True)
    first["report"]["charged_atom_indices"][:] = -1
    first["report"]["parameters"]["chemical_preparation"] = "edited"
    next(
        i
        for i in first["report"]["attribution"]["items"]
        if i["id"] == "doi:10.1021/ci990307l"
    )["authors"].append("edited")
    second = msm.physchem.get_lipophilicity(path, return_report=True)
    assert second["report"]["charged_atom_indices"].tolist() == [1, 3]
    assert second["report"]["parameters"]["chemical_preparation"] == "none"
    assert (
        "edited"
        not in next(
            i
            for i in second["report"]["attribution"]["items"]
            if i["id"] == "doi:10.1021/ci990307l"
        )["authors"]
    )
    assert before == hashlib.sha256(Path(path).read_bytes()).digest()


def test_optional_ackredit_real_session_empty_absence_and_failure(monkeypatch):
    import warnings

    from molsysmt import _ackredit

    ackredit = pytest.importorskip("ackredit")
    with (
        ackredit.session("lipophilicity consumer"),
        ackredit.scope("consumer.describe"),
    ):
        first = msm.physchem.get_lipophilicity(source("CCO"), return_report=True)
        empty = msm.physchem.get_lipophilicity(
            source("CCO"), selection=[], return_report=True
        )
        assert "doi:10.1021/ci990307l" in ackredit.get_used_items()
        tree = ackredit.current_session().usage_tree
        assert (
            "molsysmt.physchem.get_lipophilicity"
            in tree["consumer.describe"]["children"]
        )
        assert (
            "molsysmt.physchem.get_aromaticity"
            in tree["molsysmt.physchem.get_lipophilicity"]["children"]
        )
    for result in (first, empty):
        items = {i["id"]: i for i in result["report"]["attribution"]["items"]}
        assert items["doi:10.1021/ci990307l"]["roles"] == ["scientific_criterion"]
        assert result["report"]["software"]["rdkit"]
        assert result["report"]["software"]["molsysmt"]
    assert "rdkit-aromaticity-model" not in {
        i["id"] for i in empty["report"]["attribution"]["items"]
    }
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    np.testing.assert_allclose(
        msm.physchem.get_lipophilicity(source("CCO")), [-0.0014], atol=1e-12, rtol=0
    )

    def broken():
        raise RuntimeError("controlled attribution failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        np.testing.assert_allclose(
            msm.physchem.get_lipophilicity(source("CCO")), [-0.0014], atol=1e-12, rtol=0
        )


def test_unknown_sdf_hydrogen_inventory_fails(tmp_path):
    from rdkit import Chem

    path = tmp_path / "unknown.sdf"
    with Chem.SDWriter(str(path)) as writer:
        writer.write(source("CCO"))
    with pytest.raises(
        msm.StructuralInconsistencyError, match="declared n_implicit_hydrogens"
    ):
        msm.physchem.get_lipophilicity(str(path))


def test_fresh_imports_are_lazy_and_genuine_ackredit_absence_keeps_report():
    import subprocess
    import sys

    script = """
import sys
from importlib.abc import MetaPathFinder
from unittest.mock import patch
import molsysmt as msm
assert 'ackredit' not in sys.modules
assert 'rdkit' not in sys.modules
from depdigest import is_installed
from depdigest.core import checker
from rdkit import Chem
original = checker.find_spec

def absent(name, *args, **kwargs):
    return None if name == 'ackredit' else original(name, *args, **kwargs)

class RefuseAckredit(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'ackredit' or fullname.startswith('ackredit.'):
            raise ImportError('Ackredit absent in this controlled interpreter')

sys.meta_path.insert(0, RefuseAckredit())
with patch.object(checker, 'find_spec', absent):
    is_installed.cache_clear()
    result = msm.physchem.get_lipophilicity(Chem.MolFromSmiles('c1ccccc1'), return_report=True)
    assert abs(result['lipophilicity'][0] - 1.6866) < 1e-12
    assert 'doi:10.1021/ci990307l' in {item['id'] for item in result['report']['attribution']['items']}
assert 'ackredit' not in sys.modules
"""
    run = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert run.returncode == 0, run.stderr
