"""Atomic-context conservation and public hierarchical descriptor selections."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture
def molsys():
    from rdkit import Chem

    from molsysmt.native.topology import Chains_DataFrame, Groups_DataFrame

    result = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    topology = result.topology
    topology.groups = Groups_DataFrame(n_groups=2)
    topology.set_atom_molecules(None)
    topology.groups["group_name"] = ["POLAR", "ALKYL"]
    topology.groups["group_type"] = ["small molecule", "small molecule"]
    topology.groups["molecule_index"] = [0, 0]
    topology.atoms["group_index"] = [1, 0, 0]
    topology.chains = Chains_DataFrame(n_chains=2)
    topology.chains["chain_id"] = ["A", "B"]
    topology.atoms["chain_index"] = [1, 0, 0]
    topology._molecules_dirty = False
    return result


def calculate(molsys, descriptor, **kwargs):
    function = getattr(msm.physchem, f"get_{descriptor}")
    result = function(molsys, **kwargs)
    if isinstance(result, dict):
        result = result[descriptor]
    return (
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2")
        if descriptor == "tpsa"
        else result
    )


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
@pytest.mark.parametrize(
    "element,selection,membership",
    [
        ("atom", "all", [[0], [1], [2]]),
        ("atom", [2, 0, 2], [[2], [0], [2]]),
        ("group", "all", [[1, 2], [0]]),
        ("group", [1, 0, 1], [[0], [1, 2], [0]]),
        ("group", "atom_index==0", [[0]]),
        ("chain", "all", [[1, 2], [0]]),
        ("chain", [1, 0, 1], [[0], [1, 2], [0]]),
        ("component", "all", [[0, 1, 2]]),
        ("entity", "all", [[0, 1, 2]]),
        ("molecule", "all", [[0, 1, 2]]),
        ("system", [2, 0], [[2, 0]]),
    ],
)
def test_selected_elements_sum_complete_context_contributions(
    molsys, descriptor, element, selection, membership
):
    atomic = (
        np.array([0, 0, 20.23])
        if descriptor == "tpsa"
        else np.array([0.5131, 0.0425, -0.5570])
    )
    expected = [sum(atomic[atoms]) for atoms in membership]
    result = calculate(molsys, descriptor, element=element, selection=selection)
    assert np.shape(result) == (() if element == "system" else (len(membership),))
    np.testing.assert_allclose(
        result, expected[0] if element == "system" else expected, atol=1e-12, rtol=0
    )


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
@pytest.mark.parametrize(
    "element", ["atom", "group", "chain", "component", "molecule", "entity", "system"]
)
def test_empty_populations_and_indices(molsys, descriptor, element):
    result = getattr(msm.physchem, f"get_{descriptor}")(
        molsys, element=element, selection=[], return_report=True
    )
    values = result[descriptor]
    assert values.shape == (() if element == "system" else (0,))
    if element == "system":
        assert float(calculate(molsys, descriptor, element=element, selection=[])) == 0
    report = result["report"]
    assert report["element"] == element
    assert report["element_atom_indices"].dtype == np.int64
    assert report["element_atom_offsets"].tolist() == (
        [0, 0] if element == "system" else [0]
    )


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
def test_report_separates_output_membership_from_complete_calculation_context(
    molsys, descriptor
):
    function = getattr(msm.physchem, f"get_{descriptor}")
    result = function(molsys, element="atom", selection=[2, 0, 2], return_report=True)
    report = result["report"]
    assert report["element_indices"].tolist() == [2, 0, 2]
    assert report["element_atom_indices"].tolist() == [2, 0, 2]
    assert report["element_atom_offsets"].tolist() == [0, 1, 2, 3]
    assert report["molecule_indices"].tolist() == [0]
    assert report["atom_indices"].tolist() == [0, 1, 2]
    assert report["atom_offsets"].tolist() == [0, 3]
    assert report["output_kind"] == "atomic_contribution_sum"
    assert report["parameters"]["contribution_context"] == "complete_source_molecules"
    report["element_indices"][:] = -1
    assert function(molsys, element="atom", selection=[2], return_report=True)[
        "report"
    ]["element_indices"].tolist() == [2]


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
@pytest.mark.parametrize(
    "form", ["rdkit.Mol", "molsysmt.MolSys", "native_domains", "h5msm"]
)
def test_form_agnostic_atom_contributions_preserve_source(
    molsys, descriptor, form, tmp_path
):
    from rdkit import Chem

    if form == "rdkit.Mol":
        molsys = msm.convert(molsys, to_form=form)
        before = molsys.ToBinary()
    elif form == "h5msm":
        molsys = msm.convert(molsys, to_form=str(tmp_path / "source.h5msm"))
    elif form == "native_domains":
        molsys = [molsys.topology, molsys.chemical_states]
    atomic = calculate(molsys, descriptor, element="atom")
    molecular = calculate(molsys, descriptor)
    np.testing.assert_allclose(sum(atomic), molecular[0], atol=1e-12, rtol=0)
    if form == "rdkit.Mol":
        assert molsys.ToBinary() == before
        explicit = Chem.AddHs(molsys)
        expanded = calculate(explicit, descriptor, element="atom")
        folded = expanded[:3].copy()
        for atom in explicit.GetAtoms():
            if atom.GetIdx() >= 3:
                folded[atom.GetNeighbors()[0].GetIdx()] += expanded[atom.GetIdx()]
        np.testing.assert_allclose(atomic, folded, atol=1e-12, rtol=0)


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_contribution_units_follow_physical_dimension(molsys, descriptor, unit):
    with msm.pyunitwizard.context(standard_units=[unit, "ps", "radians"]):
        result = getattr(msm.physchem, f"get_{descriptor}")(molsys, element="group")
    if descriptor == "tpsa":
        assert msm.pyunitwizard.get_unit(result) == msm.pyunitwizard.unit(unit) ** 2
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(result, to_unit="angstrom**2"),
            [20.23, 0],
            atol=1e-12,
            rtol=0,
        )
    else:
        assert isinstance(result, np.ndarray)
        np.testing.assert_allclose(result, [-0.5145, 0.5131], atol=1e-12, rtol=0)


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
def test_selected_atom_cannot_hide_missing_evidence_in_its_context(molsys, descriptor):
    molsys.chemical_states._states[0].atom_attributes.loc[0, "n_implicit_hydrogens"] = (
        None
    )
    with pytest.raises(msm.StructuralInconsistencyError):
        calculate(molsys, descriptor, element="atom", selection=[2])


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
def test_structure_associated_chemistry_resolves_without_coordinate_copy(
    molsys, descriptor, monkeypatch
):
    molsys.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((3, 3, 3)), "nm")
    second = deepcopy(molsys.chemical_states._states[0])
    second.state_id = "other"
    molsys.chemical_states._append_state(second, False)
    molsys._set_structure_chemical_state_indices([0, 1, 0])

    def forbidden(*args, **kwargs):
        raise AssertionError("Descriptor context must not copy source coordinates.")

    monkeypatch.setattr(molsys.structures, "copy", forbidden)
    with pytest.raises(msm.StructuralInconsistencyError):
        calculate(
            molsys,
            descriptor,
            element="group",
            chemical_state="structure",
            structure_indices=[2, 1],
        )
    assert (
        len(
            calculate(
                molsys,
                descriptor,
                element="group",
                chemical_state="structure",
                structure_indices=[2, 0],
            )
        )
        == 2
    )


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
@pytest.mark.parametrize(
    "smiles",
    [
        "OC(=O)P(=O)(O)O",
        "CS(C)(=O)=O",
        "[NH3+]CC(=O)[O-]",
        "C[N+](=O)[O-]",
        "c1ccncc1",
        "[2H]OC",
    ],
)
@pytest.mark.parametrize("include_sp", [False, True])
def test_complete_atomic_sum_matches_original_descriptor_for_model_variants(
    descriptor, smiles, include_sp
):
    from rdkit import Chem

    molsys = Chem.MolFromSmiles(smiles)
    kwargs = {"include_sulfur_phosphorus": include_sp} if descriptor == "tpsa" else {}
    atomic = calculate(molsys, descriptor, element="atom", **kwargs)
    complete = calculate(molsys, descriptor, **kwargs)
    np.testing.assert_allclose(sum(atomic), complete[0], atol=1e-12, rtol=0)


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
def test_repeated_group_outputs_calculate_each_context_once(
    molsys, descriptor, monkeypatch
):
    from rdkit.Chem import rdMolDescriptors

    name = "_CalcTPSAContribs" if descriptor == "tpsa" else "_CalcCrippenContribs"
    original = getattr(rdMolDescriptors, name)
    calls = []

    def count(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(rdMolDescriptors, name, count)
    calculate(molsys, descriptor, element="group", selection=[1, 0, 1])
    assert len(calls) == 1


@pytest.mark.parametrize("descriptor", ["tpsa", "lipophilicity"])
def test_unselected_molecules_are_not_required_for_atomic_context(descriptor):
    from rdkit import Chem

    result = calculate(
        Chem.MolFromSmiles("CCO.[Zn+2]"), descriptor, element="atom", selection=[2]
    )
    np.testing.assert_allclose(
        result, [20.23] if descriptor == "tpsa" else [-0.557], atol=1e-12, rtol=0
    )
