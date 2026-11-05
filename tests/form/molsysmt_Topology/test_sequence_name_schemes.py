"""Project native naming declarations through public sequence conversions."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Topology


def template(names, **kwargs):
    return msm.physchem.get_peptide_chemical_template(
        names, n_terminal_state="ammonium", c_terminal_state="carboxylate", **kwargs
    )["template"]


@pytest.mark.parametrize(
    "target",
    [
        "molsysmt.MolSys",
        "molsysmt.Topology",
        "molsysmt.MolSysDict",
        "molsysmt.TopologyDict",
        "file",
    ],
)
def test_native_template_declarations_fix_sequence_without_changing_chemistry(
    target, tmp_path
):
    source = template(["GLH", "HID", "HIE", "HIP", "ASH", "CYM", "LYN"])
    bonds = source.chemical_states.get_bonds().copy(deep=True)
    names = source.topology.groups.group_name.tolist()
    assert source.topology.group_naming_schemes == ("amber",) * 7
    value = msm.convert(
        source, to_form=str(tmp_path / "peptide.h5msm") if target == "file" else target
    )
    assert msm.convert(value, to_form="string:amino_acids_1") == "EHHHDCK"
    pd.testing.assert_frame_equal(
        bonds, source.chemical_states.get_bonds(), check_frame_type=False
    )
    assert source.topology.groups.group_name.tolist() == names
    assert source.structures is None


def test_disulfide_template_retains_declared_cyx_and_bonded_chemistry():
    source = template(["CYX", "CYX"], disulfide_group_pairs=[[0, 1]])
    bonds = source.chemical_states.get_bonds().copy(deep=True)
    assert msm.convert(source, to_form="string:amino_acids_1") == "CC"
    assert source.topology.groups.group_name.tolist() == ["CYX", "CYX"]
    pd.testing.assert_frame_equal(
        bonds, source.chemical_states.get_bonds(), check_frame_type=False
    )


@pytest.mark.parametrize("sequence", ["amino_acids_1:JX", "amino_acids_3:XleXaa"])
def test_explicit_sequence_construction_declares_its_alphabet(sequence):
    source = msm.convert(sequence, to_form="molsysmt.Topology")
    assert source.n_atoms == 0
    assert source.group_naming_schemes == ("sequence", "sequence")
    assert msm.convert(source, to_form="string:amino_acids_1") == "JX"


def test_noncanonical_sequence_labels_do_not_acquire_an_invented_scheme():
    source = msm.convert("amino_acids_3:AlaGlhHid", to_form="molsysmt.Topology")
    assert source.group_naming_schemes == ("sequence", None, None)
    with pytest.raises(ArgumentError, match="context-dependent"):
        msm.convert(source, to_form="string:amino_acids_1")
    source.set_group_naming_schemes("amber", group_indices=[1, 2])
    assert msm.convert(source, to_form="string:amino_acids_1") == "AEH"


def test_mixed_native_profiles_preserve_ordered_repeated_group_positions():
    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import (
        to_string_amino_acids_1,
    )

    source = Topology(n_groups=4)
    source.groups["group_name"] = ["GLH", "GLH", "ALA", "LYN"]
    source.groups["group_type"] = ["amino acid"] * 4
    source.set_group_naming_schemes(["amber", "legacy", None, "ccd"])
    assert msm.convert(source, to_form="string:amino_acids_1") == "EQAK"
    selected = np.array([3, 0, 1, 3], dtype=np.int64)
    selected.flags.writeable = False
    assert to_string_amino_acids_1(source, group_indices=selected) == "KEQK"
    np.testing.assert_array_equal(selected, [3, 0, 1, 3])
    assert source.groups.group_name.tolist() == ["GLH", "GLH", "ALA", "LYN"]


def test_bulk_projection_credits_references_once_per_query(monkeypatch):
    from molsysmt import _ackredit

    source = template(["GLH", "HID", "HIE", "HIP"])
    calls = []

    def credit(provider, items, caller, *, contextual=False):
        calls.append((items, caller, contextual))

    monkeypatch.setattr(_ackredit, "credit", credit)
    assert msm.convert(source, to_form="string:amino_acids_1") == "EHHH"
    assert len(calls) == 1
    items, caller, contextual = calls[0]
    assert len({item["id"] for item in items}) == len(items) == 2
    assert contextual
    assert "to_string_amino_acids_1" in caller


def test_explicit_ccd_nonpeptide_cannot_be_projected_as_a_sequence_symbol():
    source = Topology(n_groups=1)
    source.groups["group_name"] = ["XLE"]
    source.groups["group_type"] = ["amino acid"]
    source.set_group_naming_schemes("ccd")
    with pytest.raises(ArgumentError, match="no supported amino-acid"):
        msm.convert(source, to_form="string:amino_acids_1")
    assert source.group_naming_schemes == ("ccd",)
