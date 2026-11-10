"""PDBFixer assessment must retain chain context before filtering group scope."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize(
    "selection,syntax",
    [([1], "MolSysMT"), ("group_index==1", "MolSysMT"), ("resid 1", "MDTraj")],
)
def test_selected_internal_group_is_not_made_a_pdbfixer_terminus(selection, syntax):
    source = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    before = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()
    result = msm.build.get_missing_terminal_cappings(
        source, selection=selection, syntax=syntax, engine="PDBFixer"
    )
    assert result == {}
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"), before
    )


def test_selected_real_pdbfixer_terminus_keeps_its_source_group_index():
    source = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    assert msm.build.get_missing_terminal_cappings(
        source, selection=[2], engine="PDBFixer"
    ) == {2: ["OXT"]}


def test_empty_group_selection_does_not_construct_a_pdbfixer_model(monkeypatch):
    source = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    import molsysmt.basic

    def forbidden(*args, **kwargs):
        pytest.fail("Empty report scope must not construct the optional detector")

    monkeypatch.setattr(molsysmt.basic, "convert", forbidden)
    assert (
        msm.build.get_missing_terminal_cappings(source, selection=[], engine="PDBFixer")
        == {}
    )


def test_detection_does_not_modify_a_supplied_pdbfixer_instance():
    source = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    fixer = msm.convert(source, to_form="pdbfixer.PDBFixer")
    assert not hasattr(fixer, "missingTerminals")
    assert msm.build.get_missing_terminal_cappings(
        fixer, selection=[2], engine="PDBFixer"
    ) == {2: ["OXT"]}
    assert not hasattr(fixer, "missingTerminals")
