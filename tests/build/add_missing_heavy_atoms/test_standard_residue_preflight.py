"""Protecting bounded standard-residue placement independently of atom-count parity."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    UnassessedResidueWarning,
)


def incomplete_serine():
    source = msm.build.build_peptide("Ser", engine="MolSysMT")
    return msm.extract(source, selection='atom_type != "H" and atom_name != "OG"')


def test_observed_lysine_gaps_stay_unassessed_while_serine_is_repaired():
    path = (
        Path(__file__).resolve().parents[2]
        / "physchem/data/chemical_templates/1qku.cif.gz"
    )
    full = msm.convert(path, to_form="molsysmt.MolSys")
    source = msm.extract(
        full, selection='molecule_type == "protein" and chain_id == "A"'
    )
    original = source.copy()
    assert msm.build.get_missing_heavy_atoms(source) == {
        0: ["OG"],
        1: ["CD", "CE", "CG", "NZ"],
        2: ["CD", "CE", "CG", "NZ"],
    }
    with pytest.warns(
        (UnassessedResidueWarning, StructuralAttributeDropWarning)
    ) as caught:
        repaired = msm.build.add_missing_heavy_atoms(source)
    ambiguous = [
        w.message for w in caught if isinstance(w.message, UnassessedResidueWarning)
    ]
    assert len(ambiguous) == 2
    assert all("multiple missing side-chain atoms" in str(w) for w in ambiguous)
    assert repaired.get_n_atoms() == 1991
    assert msm.build.get_missing_heavy_atoms(repaired) == {
        1: ["CD", "CE", "CG", "NZ"],
        2: ["CD", "CE", "CG", "NZ"],
    }
    mapping = pd.Index(repaired.topology.atoms.atom_id).get_indexer(
        original.topology.atoms.atom_id
    )
    assert (mapping >= 0).all()
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(repaired.structures.coordinates, to_unit="nm")[
            :, mapping
        ],
        msm.pyunitwizard.get_value(original.structures.coordinates, to_unit="nm"),
    )
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    assert source.structures.b_factor is not None


@pytest.mark.parametrize(
    "variant", ["collinear", "nonfinite", "wrong_element", "duplicate"]
)
def test_invalid_standard_residue_anchors_or_identity_leave_source_unchanged(variant):
    source = incomplete_serine()
    if variant == "collinear":
        source.structures.coordinates = msm.pyunitwizard.quantity(
            np.arange(source.get_n_atoms() * 3).reshape(1, -1, 3), "angstrom"
        )
    elif variant == "nonfinite":
        xyz = msm.pyunitwizard.get_value(source.structures.coordinates).copy()
        xyz[0, 0, 0] = np.nan
        source.structures.coordinates = msm.pyunitwizard.quantity(xyz, "nm")
    elif variant == "wrong_element":
        source.topology.atoms.loc[
            source.topology.atoms.atom_name.eq("CB"), "atom_type"
        ] = "Na"
    else:
        source.topology.atoms.at[0, "atom_name"] = "CA"
    original = source.topology.atoms.copy(deep=True)
    with pytest.warns(UnassessedResidueWarning):
        repaired = msm.build.add_missing_heavy_atoms(source)
    pd.testing.assert_frame_equal(repaired.topology.atoms, original)
    pd.testing.assert_frame_equal(source.topology.atoms, original)
    assert repaired.get_n_atoms() == source.get_n_atoms()
