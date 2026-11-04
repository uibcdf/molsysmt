"""Keeping peptide-end cap classification separate from connecting atom roles."""

import numpy as np
import pytest

import molsysmt as msm


def _capped_alanine(c_terminal, *, same_chain=True):
    builder = msm.MolSysBuilder()
    names = [
        ("ACE", [("CH3", "C"), ("C", "C"), ("O", "O")]),
        ("ALA", [("N", "N"), ("CA", "C"), ("C", "C"), ("O", "O"), ("CB", "C")]),
        (
            c_terminal,
            [("N", "N"), ("CH3", "C")] if c_terminal == "NME" else [("N", "N")],
        ),
    ]
    groups = []
    for name, atoms in names:
        indices = [
            builder.add_atom(atom_name=label, atom_type=element)
            for label, element in atoms
        ]
        groups.append(builder.add_group(indices, group_name=name))
    if same_chain:
        builder.add_chain(groups, chain_id="A")
    else:
        for group in groups:
            builder.add_chain([group])
    coordinates = np.zeros((1, builder.topology.n_atoms, 3))
    coordinates[0, :, 0] = np.arange(builder.topology.n_atoms)
    coordinates[0, 1, 0] = -0.133
    coordinates[0, 3, 0] = 0.0
    coordinates[0, 5, 0] = 0.30
    coordinates[0, 8, 0] = 0.433
    builder.set_coordinates(msm.pyunitwizard.quantity(coordinates, "nm"))
    return builder.build()


@pytest.mark.parametrize("cap", ["NME", "NHE", "NH2"])
@pytest.mark.parametrize("selection", ["all", [1, 3, 5, 8]])
def test_caps_keep_their_backbone_connection_candidates(cap, selection):
    source = _capped_alanine(cap)
    before = msm.pyunitwizard.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    observed = msm.build.get_missing_bonds(source, selection=selection, pbc=False)
    assert [1, 3] in observed  # ACE.C to ALA.N
    assert [5, 8] in observed  # ALA.C to the C-terminal cap N
    assert msm.get(source, n_bonds=True) == 0
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(msm.get(source, coordinates=True), to_unit="nm"),
        before,
    )


@pytest.mark.parametrize("cap", ["NME", "NHE", "NH2"])
def test_caps_in_separate_chains_do_not_create_peptide_candidates(cap):
    observed = msm.build.get_missing_bonds(
        _capped_alanine(cap, same_chain=False), pbc=False
    )
    assert [1, 3] not in observed
    assert [5, 8] not in observed


@pytest.mark.parametrize("cap", ["NME", "NHE", "NH2"])
def test_template_only_cap_candidates_do_not_require_coordinates(cap):
    source = _capped_alanine(cap)
    source.structures = None
    observed = msm.build.get_missing_bonds(source, with_distances=False)
    assert [0, 1] in observed and [1, 2] in observed
    assert [1, 3] not in observed and [5, 8] not in observed
