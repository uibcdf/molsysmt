"""Reject unknown PDB grouping prerequisites without repairing the source (#525)."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import NotCompatibleConversionError


@pytest.fixture
def molsys():
    return msm.convert(
        msm.systems["Trp-Cage"]["1l2y.pdb"],
        selection=[0, 1, 2],
        structure_indices=[0],
        to_form="molsysmt.MolSys",
    )


@pytest.mark.parametrize("membership", ["group_index", "chain_index"])
def test_missing_membership_rejected_without_mutating_source(molsys, membership):
    molsys.topology.atoms.loc[1, membership] = pd.NA
    tables = {
        name: getattr(molsys.topology, name).copy(deep=True)
        for name in ("atoms", "groups", "molecules", "entities", "chains")
    }
    coordinates = molsys.structures.coordinates.copy()
    bonds = molsys.chemical_states.get_bonds().copy(deep=True)

    with pytest.raises(NotCompatibleConversionError, match=membership):
        msm.convert(molsys, to_form="string:pdb_text")

    for name, expected in tables.items():
        pd.testing.assert_frame_equal(getattr(molsys.topology, name), expected)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates),
        msm.pyunitwizard.get_value(coordinates),
    )
    assert msm.pyunitwizard.get_unit(
        molsys.structures.coordinates
    ) == msm.pyunitwizard.get_unit(coordinates)
    pd.testing.assert_frame_equal(molsys.chemical_states.get_bonds(), bonds)


def test_reported_legacy_h5msm_has_actionable_chain_diagnostic():
    molsys = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        selection=list(range(10)),
        structure_indices=[0],
        to_form="molsysmt.MolSys",
    )
    assert msm.get(molsys, element="atom", chain_index=True) == [None] * 10
    with pytest.raises(NotCompatibleConversionError, match="chain_index"):
        msm.convert(molsys, to_form="string:pdb_text")


@pytest.mark.parametrize("membership", ["group_index", "chain_index"])
def test_unknown_membership_outside_selection_does_not_block_export(molsys, membership):
    molsys.topology.atoms.loc[1, membership] = pd.NA
    text = msm.convert(molsys, selection=[0, 2], to_form="string:pdb_text")
    records = [
        line for line in text.splitlines() if line.startswith(("ATOM  ", "HETATM"))
    ]
    assert len(records) == 2
    assert pd.isna(molsys.topology.atoms.loc[1, membership])


def test_assigned_unnamed_chain_is_distinct_from_unknown_membership(molsys):
    molsys.topology.chains.loc[0, "chain_name"] = pd.NA
    text = msm.convert(molsys, to_form="string:pdb_text")
    records = [
        line for line in text.splitlines() if line.startswith(("ATOM  ", "HETATM"))
    ]
    assert len(records) == 3
    assert all(line[21] == "A" for line in records)
    assert molsys.topology.atoms["chain_index"].tolist() == [0, 0, 0]
    assert pd.isna(molsys.topology.chains.loc[0, "chain_name"])


@pytest.mark.parametrize("existing", [False, True])
def test_failed_file_export_does_not_create_or_overwrite_destination(
    molsys, tmp_path, existing
):
    molsys.topology.atoms.loc[1, "chain_index"] = pd.NA
    destination = tmp_path / "output.pdb"
    if existing:
        destination.write_text("preserve this destination\n")
    with pytest.raises(NotCompatibleConversionError, match="chain_index"):
        msm.convert(molsys, to_form="file:pdb", output_filename=destination)
    if existing:
        assert destination.read_text() == "preserve this destination\n"
    else:
        assert not destination.exists()
