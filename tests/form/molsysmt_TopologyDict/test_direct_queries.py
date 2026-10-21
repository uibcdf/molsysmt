"""Protecting stored atom reads and the declarative finalization fallback."""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.fixture(params=[msm.TopologyDict, msm.MolSysDict])
def stored_atoms(request):
    topology = {
        "atoms": [
            {"atom_id": "10", "atom_name": "N", "atom_type": "N"},
            {"atom_id": "20", "atom_name": "CA", "atom_type": "C"},
            {"atom_id": "30", "atom_name": "O", "atom_type": "O"},
        ]
    }
    if request.param is msm.MolSysDict:
        return request.param(data={"topology": topology})
    return request.param(data=topology)


def test_stored_atom_queries_do_not_build_or_copy(stored_atoms, monkeypatch):
    topology = stored_atoms.data.get("topology", stored_atoms.data)
    # Defaults outside the actual selection must not force bulk reconstruction.
    topology["atoms"][1]["atom_type"] = None

    def forbid(*args, **kwargs):
        raise AssertionError("Stored atom queries must not reconstruct native data.")

    monkeypatch.setattr(msm.MolSysBuilder, "__init__", forbid)
    monkeypatch.setattr(type(stored_atoms), "to_dict", forbid)
    monkeypatch.setattr(msm, "convert", forbid)

    assert msm.get(stored_atoms, n_atoms=True) == 3
    result = msm.get(
        stored_atoms,
        element="atom",
        selection=[2, 0, 2],
        atom_index=True,
        atom_id=True,
        atom_name=True,
        atom_type=True,
        n_atoms=True,
        output_type="dictionary",
    )
    assert result == {
        "atom_index": [2, 0, 2],
        "atom_id": ["30", "10", "30"],
        "atom_name": ["O", "N", "O"],
        "atom_type": ["O", "N", "O"],
        "n_atoms": 3,
    }
    assert msm.get(
        stored_atoms,
        element="atom",
        selection=[2, 0, 2],
        mask=[True, False, True],
        atom_index=True,
        atom_name=True,
    ) == [[0, 2], ["N", "O"]]
    assert msm.get(stored_atoms, element="atom", selection=[], atom_name=True) == []


def test_stored_results_are_detached_and_observe_edits(stored_atoms):
    names = msm.get(stored_atoms, element="atom", atom_name=True)
    names[0] = "changed output"
    topology = stored_atoms.data.get("topology", stored_atoms.data)
    assert topology["atoms"][0]["atom_name"] == "N"
    topology["atoms"][0]["atom_name"] = "edited input"
    assert msm.get(stored_atoms, element="atom", atom_name=True) == [
        "edited input",
        "CA",
        "O",
    ]


@pytest.mark.parametrize("selection", [[-1], [3], [0.5], [True]])
def test_stored_queries_preserve_public_index_validation(stored_atoms, selection):
    with pytest.raises(ArgumentError):
        msm.get(stored_atoms, element="atom", selection=selection, atom_name=True)


def test_nested_selections_keep_existing_route(stored_atoms):
    assert msm.get(
        stored_atoms, element="atom", selection=[[2, 0], [0, 1]], atom_name=True
    ) == [["O", "N"], ["N", "CA"]]


def test_missing_atom_fields_keep_native_defaults_and_inference(stored_atoms):
    topology = stored_atoms.data.get("topology", stored_atoms.data)
    topology["atoms"][0].pop("atom_id")
    topology["atoms"][0].pop("atom_type")
    topology["atoms"][1]["atom_id"] = 123
    expected = {"atom_id": ["0", "123", "30"], "atom_type": ["N", "C", "O"]}
    assert (
        msm.get(
            stored_atoms,
            element="atom",
            atom_id=True,
            atom_type=True,
            output_type="dictionary",
        )
        == expected
    )


def test_hierarchy_counts_still_finalize_missing_parents(stored_atoms):
    # These are not the lengths of absent groups/chains/molecules lists.
    assert msm.get(stored_atoms, n_groups=True, n_chains=True) == [3, 1]
    assert msm.get(stored_atoms, n_molecules=True) == 3


@pytest.mark.parametrize("cls", [msm.TopologyDict, msm.MolSysDict])
def test_empty_stored_inventory(cls):
    item = cls()
    assert msm.get(item, n_atoms=True) == 0
    assert msm.get(item, element="atom", atom_name=True, atom_index=True) == [[], []]
