"""Testing exhaustive native builder conversion reports."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _add_reduced_schema_losses(molsys):
    output = molsys.copy()
    msm.set(
        output,
        element="atom",
        selection=[0],
        formal_charge=[1],
    )
    msm.set(
        output,
        element="bond",
        selection=[0],
        fractional_bond_order=[1.5],
    )
    velocities = np.ones_like(
        puw.get_value(output.structures.coordinates, to_unit="nm")
    )
    output.structures.set_velocities(
        value=puw.quantity(velocities, "nm/ps"),
        skip_digestion=True,
    )
    return output


def test_molsys_and_builder_preserve_topology_and_structures(rich_molsys):
    source = _add_reduced_schema_losses(rich_molsys)

    builder, report = msm.convert(
        source,
        to_form="molsysmt.MolSysBuilder",
        return_report=True,
    )

    assert report.audited_scopes == ("all",)
    assert report.is_exhaustive
    assert report.outcome == "equivalent"
    formal_charge = msm.get(builder, formal_charge=True)
    assert formal_charge[0] == 1
    assert all(pd.isna(value) for value in formal_charge[1:])
    assert puw.get_value(
        msm.get(builder, velocities=True),
        to_unit="nm/ps",
    ).shape == (3, 4, 3)

    rebuilt, rebuilt_report = msm.convert(
        builder,
        to_form="molsysmt.MolSys",
        return_report=True,
    )

    assert rebuilt_report.audited_scopes == ("all",)
    assert rebuilt_report.is_exhaustive
    assert rebuilt_report.outcome == "equivalent"
    assert msm.get(rebuilt, formal_charge=True)[0] == 1


def test_molsys_to_builder_reports_mechanics_loss_and_rejects_strict(
    rich_molsys,
):
    source = rich_molsys.copy()
    source.molecular_mechanics.partial_charge = np.array(
        [0.1, 0.2, -0.2, -0.1]
    )
    source.molecular_mechanics.forcefield = "test-forcefield"

    _, report = msm.convert(
        source,
        to_form="molsysmt.MolSysBuilder",
        return_report=True,
    )

    assert report.is_exhaustive
    assert report.outcome == "lossy"
    assert {"partial_charge", "forcefield"} <= {
        issue.attribute for issue in report.issues
    }
    with pytest.raises(msm.NotCompatibleConversionError, match="partial_charge"):
        msm.convert(
            source,
            to_form="molsysmt.MolSysBuilder",
            strict=True,
        )


def test_molsys_to_builder_distinguishes_implicit_and_explicit_associations(
    rich_molsys,
):
    implicit = rich_molsys.copy()
    implicit._set_structure_chemical_state_indices([0, 0, 0])

    _, implicit_report = msm.convert(
        implicit,
        to_form="molsysmt.MolSysBuilder",
        return_report=True,
    )
    assert implicit_report.is_exhaustive
    assert implicit_report.outcome == "equivalent"

    explicit = rich_molsys.copy()
    explicit.topology._append_chemical_state(state_id="alternate")
    explicit._set_structure_chemical_state_indices([0, 1, 1])

    builder, explicit_report = msm.convert(
        explicit,
        to_form="molsysmt.MolSysBuilder",
        return_report=True,
    )
    assert explicit_report.is_exhaustive
    assert explicit_report.outcome == "lossy"
    assert (
        "structure_chemical_state_index",
        "state_association_loss",
    ) in {
        (issue.attribute, issue.kind)
        for issue in explicit_report.issues
    }
    assert msm.get(builder, n_chemical_states=True) == 2

    with pytest.raises(
        msm.NotCompatibleConversionError,
        match="structure_chemical_state_index",
    ):
        msm.convert(
            explicit,
            to_form="molsysmt.MolSysBuilder",
            strict=True,
        )


def test_builder_to_molsysdict_audits_the_reduced_schema(rich_molsys):
    source = _add_reduced_schema_losses(rich_molsys)
    source.topology.atoms.loc[0, "isotope"] = 13
    builder = msm.convert(source, to_form="molsysmt.MolSysBuilder")

    payload, report = msm.convert(
        builder,
        to_form="molsysmt.MolSysDict",
        return_report=True,
    )

    assert report.audited_scopes == ("all",)
    assert report.is_exhaustive
    assert report.outcome == "lossy"
    issues = {issue.attribute: issue for issue in report.issues}
    assert issues["formal_charge"].scope == "chemical_state"
    assert issues["fractional_bond_order"].scope == "chemical_state"
    assert issues["velocities"].scope == "structures"
    assert payload.to_dict(copy=False)["topology"]["atoms"][0]["isotope"] == 13

    with pytest.raises(msm.NotCompatibleConversionError, match="velocities"):
        msm.convert(
            builder,
            to_form="molsysmt.MolSysDict",
            strict=True,
        )


def test_molsysdict_to_builder_is_exhaustive_and_materializes_components(
    rich_molsys,
):
    builder = msm.convert(
        rich_molsys,
        to_form="molsysmt.MolSysBuilder",
    )
    selected_dict, report = msm.convert(
        builder,
        to_form="molsysmt.MolSysDict",
        selection=[2, 0],
        structure_indices=[2, 0],
        return_report=True,
    )

    assert report.is_exhaustive
    assert report.outcome == "lossy"
    payload = selected_dict.to_dict(copy=False)
    assert [
        atom["atom_id"] for atom in payload["topology"]["atoms"]
    ] == ["100", "102"]
    assert payload["structures"]["structure_id"] == [50, 10]

    rebuilt, rebuilt_report = msm.convert(
        selected_dict,
        to_form="molsysmt.MolSysBuilder",
        return_report=True,
    )

    assert rebuilt_report.audited_scopes == ("all",)
    assert rebuilt_report.is_exhaustive
    assert rebuilt_report.outcome == "equivalent"
    assert msm.get(rebuilt, element="atom", atom_id=True) == ["100", "102"]
    assert msm.get(rebuilt, structure_id=True) == ["50", "10"]
    assert msm.has_attribute(rebuilt, "component_index")
    assert msm.get(rebuilt, element="atom", component_index=True) == [0, 0]
