"""Default-reference SMARTS selections retain populations, roles and source axes."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, UnsupportedHeavyOperationError
from molsysmt.native import Structures

PATTERNS = ["[#6]", "[#6]-[Cl]", "[O]=[C]"]
READERS = ["smarts", "hydrophobic", "halogen"]


def declared_system(smiles="CCC.CCl.C=O"):
    source = msm.convert(Chem.MolFromSmiles(smiles), to_form="molsysmt.MolSys")
    memberships = msm.get(source, element="molecule", atom_index=True)
    builder = msm.MolSysBuilder(source)
    groups = [
        builder.add_group(atoms, group_name="LIG", group_id=str(10 + index))
        for index, atoms in enumerate(memberships)
    ]
    builder.add_chain(groups, chain_id="A")
    source = builder.build()
    assert msm.get(source, n_molecules=True) == len(memberships)
    np.testing.assert_equal(
        msm.get(source, element="molecule", atom_index=True), memberships
    )
    count = source.topology.n_atoms
    source.topology.atoms["atom_name"] = [f"A{i}" for i in range(count)]
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(3 * count * 3, dtype=float).reshape(3, count, 3) / 100, "nm"
        )
    )
    return source


@pytest.fixture
def chemical_system():
    return declared_system()


def read(reader, source, **kwargs):
    if reader == "smarts":
        return msm.chemical_states.get_substructure_matches(source, PATTERNS, **kwargs)
    if reader == "hydrophobic":
        return msm.physchem.get_hydrophobic_sites(source, **kwargs)
    return msm.physchem.get_halogen_bond_sites(source, **kwargs)


def assert_population(reader, result, selected):
    key = "selection_atom_indices" if reader == "smarts" else "selected_atom_indices"
    assert result[key].tolist() == selected
    assert result[key].dtype == np.int64
    source_key = "source_atom_indices" if reader == "smarts" else "atom_source_indices"
    assert result[source_key].tolist() == list(range(7))
    if reader == "smarts":
        expected = [[[i] for i in [0, 1, 2, 3, 5]], [[3, 4]], [[6, 5]]]
        for array, matches, width in zip(result["matches"], expected, [1, 2, 2]):
            kept = [row for row in matches if all(index in selected for index in row)]
            np.testing.assert_array_equal(
                array, np.asarray(kept, dtype=np.int64).reshape(-1, width)
            )
            assert array.dtype == np.int64
    elif reader == "hydrophobic":
        # Only the central CH2 qualifies; terminal methyls and carbonyl do not.
        assert result["hydrophobic_atom_indices"].tolist() == (
            [1] if 1 in selected else []
        )
    else:
        for key, pair in [
            ("donor_halogen_pairs", [3, 4]),
            ("acceptor_reference_pairs", [6, 5]),
        ]:
            expected = [pair] if all(index in selected for index in pair) else []
            np.testing.assert_array_equal(
                result[key], np.asarray(expected, dtype=np.int64).reshape(-1, 2)
            )
            assert result[key].dtype == np.int64


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("chemical_state", [None, "reference"])
@pytest.mark.parametrize("form", ["native", "complementary", "h5msm"])
@pytest.mark.parametrize(
    "query,selected",
    [
        ("all and all", list(range(7))),
        ("name ZZZX", []),
        ("index 3 4 5 6", [3, 4, 5, 6]),
        ("name A1", [1]),
        ("name A6", [6]),
    ],
)
def test_default_reference_external_smarts_population(
    chemical_system, reader, chemical_state, form, query, selected, tmp_path
):
    pytest.importorskip("mdtraj")
    source = chemical_system
    if form == "complementary":
        source = [source.topology, source.chemical_states, source.structures]
    elif form == "h5msm":
        source = tmp_path / "chemical.h5msm"
        msm.convert(chemical_system, to_form=source)
    atoms = chemical_system.topology.atoms.copy(deep=True)
    states = msm.convert(
        chemical_system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    file_bytes = source.read_bytes() if form == "h5msm" else None
    kwargs = dict(chemical_state=chemical_state, structure_indices=[2, 0, 2])
    numeric = read(reader, source, selection=selected[::-1] + selected, **kwargs)
    result = read(reader, source, selection=query, syntax="MDTraj", **kwargs)
    assert_population(reader, numeric, selected)
    assert_population(reader, result, selected)
    assert result["chemical_state_index"] == 0
    pd.testing.assert_frame_equal(chemical_system.topology.atoms, atoms)
    np.testing.assert_equal(
        states,
        msm.convert(
            chemical_system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
    )
    if form == "h5msm":
        assert source.read_bytes() == file_bytes
    if selected:
        key = (
            "selection_atom_indices" if reader == "smarts" else "selected_atom_indices"
        )
        result[key][:] = -1
        assert numeric[key].tolist() == selected


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("chemical_state", [None, "reference"])
def test_explicit_inventory_and_chemistry_reference_selections(
    chemical_system, reader, chemical_state
):
    pytest.importorskip("mdtraj")
    result = read(
        reader,
        [chemical_system.topology, chemical_system.chemical_states],
        selection="all and all",
        chemical_state=chemical_state,
        syntax="MDTraj",
    )
    assert_population(reader, result, list(range(7)))


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("chemical_state", [None, "reference"])
@pytest.mark.parametrize("form", ["native", "complementary", "h5msm"])
def test_nonzero_reference_does_not_follow_structure_association(
    chemical_system, reader, chemical_state, form, tmp_path
):
    pytest.importorskip("mdtraj")
    states = chemical_system.chemical_states
    states._append_state(deepcopy(states._states[0]), set_as_reference=True)
    msm.set(chemical_system, structure_chemical_state_index=[0, 0, 0])
    source = chemical_system
    if form == "complementary":
        source = [source.topology, source.chemical_states, source.structures]
    elif form == "h5msm":
        source = tmp_path / "nonzero-reference.h5msm"
        msm.convert(chemical_system, to_form=source)
    file_bytes = source.read_bytes() if form == "h5msm" else None
    result = read(
        reader,
        source,
        selection="all and all",
        syntax="MDTraj",
        chemical_state=chemical_state,
        structure_indices=[2, 0],
    )
    assert_population(reader, result, list(range(7)))
    assert result["chemical_state_index"] == 1
    assert states.reference_chemical_state_index == 1
    assert msm.get(chemical_system, structure_chemical_state_index=True) == [0, 0, 0]
    if form == "h5msm":
        assert source.read_bytes() == file_bytes


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("state_request", [0, 1, "structure"])
def test_explicit_and_associated_state_restrictions_remain(
    chemical_system, reader, state_request
):
    pytest.importorskip("mdtraj")
    states = chemical_system.chemical_states
    states._append_state(deepcopy(states._states[0]), set_as_reference=True)
    msm.set(chemical_system, structure_chemical_state_index=[0, 1, 0])
    with pytest.raises(ArgumentError, match="syntax"):
        read(
            reader,
            chemical_system,
            selection="all and all",
            syntax="MDTraj",
            chemical_state=state_request,
            structure_indices=[0],
        )
    numeric = read(
        reader,
        chemical_system,
        selection=[0, 1, 2],
        chemical_state=state_request,
        structure_indices=[0],
    )
    assert_population(reader, numeric, [0, 1, 2])
    assert numeric["chemical_state_index"] == (
        0 if state_request == "structure" else state_request
    )


@pytest.mark.parametrize("reader", READERS)
@pytest.mark.parametrize("selection,syntax", [([1], "MolSysMT"), ("name A1", "MDTraj")])
def test_full_source_match_limits_apply_before_selection(reader, selection, syntax):
    pytest.importorskip("mdtraj")
    source = declared_system("CCCC.CCl.CCl.C=O")
    with pytest.raises(UnsupportedHeavyOperationError):
        read(reader, source, selection=selection, syntax=syntax, max_matches=1)
