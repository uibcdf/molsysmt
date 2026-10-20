"""Protect explicit stereo transfer without certifying an undeclared stereoisomer."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError

from .test_chemical_template import PROVENANCE, _options, _source, _template


def test_explicit_unspecified_is_transferred_and_retained_in_history(tmp_path):
    template = _template()
    template._chemical_states_domain._states[0].set_atom_attribute(
        "stereochemistry", ["unspecified"] * 6
    )
    source = _source(template)
    before = source.copy()
    output = msm.physchem.apply_chemical_template(source, **_options(source, template))
    result, report = output["molecular_system"], output["report"]
    assert (
        result.chemical_states._states[0].atom_attributes["stereochemistry"].tolist()
        == ["unspecified"] * 6
    )
    assigned = [r for r in report["assigned_fields"] if r["field"] == "stereochemistry"]
    assert len(assigned) == 6
    assert all(r["origin"] == "declared_template" for r in assigned)
    assert report["template_provenance"] == PROVENANCE
    assert report["atom_correspondence"].tolist() == [[i, i] for i in range(6)]
    assert report["software"]["molsysmt"]
    assert report["attribution"]["items"]
    assert "stereogenicity" in report["unassessed_checks"]
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates),
        msm.pyunitwizard.get_value(source.structures.coordinates),
    )
    # The complete achiral context is admitted; H permutations remain bounded.
    correspondence = msm.topology.get_atom_correspondences(result, selection=[0, 1])
    assert correspondence["atom_correspondences"].tolist() == [[[0, 0], [1, 1]]]
    repeated = msm.physchem.assess_chemical_template(
        result, **_options(result, template)
    )
    assert repeated["status"] == "compatible"
    assert not repeated["assigned_fields"]
    path = tmp_path / "declared-stereo.h5msm"
    msm.convert(result, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    pd.testing.assert_frame_equal(
        restored.chemical_states._states[0].atom_attributes,
        result.chemical_states._states[0].atom_attributes,
    )
    history = restored.chemical_states.get_preparation_history()
    retained = history[-1]["report"]
    assert retained["template_provenance"] == PROVENANCE
    assert [
        r for r in retained["assigned_fields"] if r["field"] == "stereochemistry"
    ] == assigned


@pytest.mark.parametrize(
    "source_label,template_label", [("R", "unspecified"), ("unspecified", "S")]
)
def test_explicit_stereo_conflicts_cannot_be_overwritten(source_label, template_label):
    source, template = _source(), _template()
    source.chemical_states._states[0].set_atom_attribute(
        "stereochemistry", [source_label] + [None] * 5
    )
    template._chemical_states_domain._states[0].set_atom_attribute(
        "stereochemistry", [template_label] + [None] * 5
    )
    before = deepcopy(source.chemical_states._states[0].atom_attributes)
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **_options(source, template))
    assert error.value.report["status"] == "conflict"
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before
    )


@pytest.mark.parametrize("label", [None, "unknown", "unsupported"])
def test_missing_unknown_and_unsupported_do_not_certify_correspondence(label):
    source, template = _source(), _template()
    if label == "unsupported":
        with pytest.raises(StructuralInconsistencyError, match="stereochemistry"):
            template._chemical_states_domain._states[0].set_atom_attribute(
                "stereochemistry", [label] * 6
            )
        return
    template._chemical_states_domain._states[0].set_atom_attribute(
        "stereochemistry", [label] * 6
    )
    options = _options(source, template)
    result = msm.physchem.apply_chemical_template(source, **options)["molecular_system"]
    with pytest.raises(StructuralInconsistencyError, match="stereochemistry"):
        msm.topology.get_atom_correspondences(result)


@pytest.mark.parametrize("smiles", ["CC(O)F", "FC=CF"])
def test_explicit_unspecified_does_not_assign_potential_stereo(smiles):
    from rdkit import Chem

    template = msm.convert(Chem.MolFromSmiles(smiles), to_form="molsysmt.MolSys")
    source = template.copy()
    source.chemical_states._states[0].atom_attributes.drop(
        columns="stereochemistry", inplace=True
    )
    n_atoms = source.get_n_atoms()
    result = msm.physchem.apply_chemical_template(
        source,
        template=template,
        atom_correspondence=np.column_stack((np.arange(n_atoms), np.arange(n_atoms))),
        template_provenance={**PROVENANCE, "hydrogen_policy": "stored_counts"},
    )["molecular_system"]
    with pytest.raises(StructuralInconsistencyError, match="stereochemistry"):
        msm.topology.get_atom_correspondences(result)


def test_benzamidinium_template_hydrogens_and_heavy_correspondences():
    from rdkit import Chem
    from rdkit.Chem import AllChem

    molecule = Chem.AddHs(Chem.MolFromSmiles("NC(=[NH2+])c1ccccc1"))
    assert AllChem.EmbedMolecule(molecule, randomSeed=390) == 0
    template = msm.convert(Chem.RemoveHs(molecule), to_form="molsysmt.MolSys")
    source = template.copy()
    state = source.chemical_states._states[0]
    state.atom_attributes = pd.DataFrame(index=range(9))
    state.bonds = state.bonds.iloc[:0].copy()
    state.connectivity_completeness = "unavailable"
    before = source.copy()
    template_before = template.copy()
    prepared = msm.physchem.apply_chemical_template(
        source,
        template=template,
        atom_correspondence=np.column_stack((np.arange(9), np.arange(9))),
        template_provenance={
            **PROVENANCE,
            "identity": "declared benzamidinium",
            "hydrogen_policy": "stored_counts",
        },
        connectivity_policy="complete_from_template",
    )["molecular_system"]
    hydrogenated = msm.build.add_missing_hydrogens(
        prepared, pH=None, engine="RDKit", mode="fixed_chemical_state"
    )
    assert hydrogenated.get_n_atoms() == 18
    result = msm.topology.get_atom_correspondences(
        hydrogenated, selection=list(range(9))
    )
    assert result["atom_correspondences"].shape == (2, 9, 2)
    assert np.all(result["atom_correspondences"][:, :3, 1] == [0, 1, 2])
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(hydrogenated.structures.coordinates)[:, :9],
        msm.pyunitwizard.get_value(before.structures.coordinates),
    )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    pd.testing.assert_frame_equal(
        template.chemical_states._states[0].atom_attributes,
        template_before.chemical_states._states[0].atom_attributes,
    )
