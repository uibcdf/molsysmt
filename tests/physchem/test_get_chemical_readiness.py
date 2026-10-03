"""Protecting honest chemical coverage, source correspondence and read-only audits."""

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures, Topology


@pytest.fixture
def chain():
    topology = Topology(n_atoms=4)
    topology.atoms["atom_type"] = ["C", "C", "O", "H"]
    topology.atoms["atom_id"] = ["a", "b", "c", "d"]
    topology.bonds = pd.DataFrame(
        {
            "atom1_index": [0, 1, 2],
            "atom2_index": [1, 2, 3],
            "bond_type": ["covalent"] * 3,
            "bond_order": [1, 1, 1],
            "evidence": ["explicit", "inferred", "unknown"],
        }
    )
    state = topology._chemical_states_domain._states[0]
    state.connectivity_completeness = "complete"
    state.set_atom_attribute("formal_charge", [0, 0, 0, 0])
    state.set_atom_attribute("n_explicit_hydrogens", [3, 2, 0, 0])
    state.provenance_index = 2
    return topology


def test_caffeine_reports_presence_without_claiming_chemical_validation():
    molsys = msm.convert(
        msm.systems["caffeine"]["caffeine.sdf"], to_form="molsysmt.MolSys"
    )
    before = msm.convert(
        molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    coords = msm.pyunitwizard.get_value(
        molsys.structures.coordinates, to_unit="nm"
    ).copy()
    report = msm.physchem.get_chemical_readiness(molsys)
    assert report["schema"] == "molsysmt.chemical_readiness@1"
    assert "ready" not in report
    assert report["chemical_state_status"] == "resolved"
    assert report["fields"]["formal_charge"]["status"] == "present"
    assert set(report["fields"]["formal_charge"]["origin"]) == {"unassessed"}
    assert report["fields"]["coordinates"]["values"].tolist() == [True] * 24
    assert report["connectivity"]["declared_completeness"] == "complete"
    assert report["explicit_hydrogen_atom_indices"].tolist() == list(range(14, 24))
    assert report["fields"]["n_implicit_hydrogens"]["status"] == "missing"
    assert {"valence", "missing_hydrogen_inventory", "docking_readiness"} <= set(
        report["unassessed_checks"]
    )
    np.testing.assert_equal(
        msm.convert(
            molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        before,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm"), coords
    )


def test_partial_unsupported_and_inferred_chemistry_are_distinct(chain):
    state = chain._chemical_states_domain._states[0]
    state.connectivity_completeness = "partial"
    chain.atoms.loc[0, "atom_type"] = "OA"
    state.set_atom_attribute("formal_charge", [0, None, -1, 0])
    state.bonds.loc[1, "bond_order"] = 0
    report = msm.physchem.get_chemical_readiness(chain)
    assert report["fields"]["atom_type"]["unsupported_indices"].tolist() == [0]
    assert report["fields"]["formal_charge"]["status"] == "partial"
    assert report["fields"]["formal_charge"]["missing_indices"].tolist() == [1]
    assert report["fields"]["covalent_multiplicity"][
        "unsupported_indices"
    ].tolist() == [1]
    assert report["connectivity"]["declared_completeness"] == "partial"
    assert report["fields"]["bond_type"]["origin"].tolist() == [
        "explicit",
        "inferred",
        "unassessed",
    ]
    # Edge evidence does not establish how order, stereo or aromaticity arose.
    assert set(report["fields"]["bond_order"]["origin"]) == {"unassessed"}
    assert report["fields"]["coordinates"]["status"] == "missing"
    assert report["state_provenance_index"] == 2


def test_selection_reports_incident_bonds_and_unobserved_hydrogen_inventory(chain):
    report = msm.physchem.get_chemical_readiness(chain, selection=[2, 1, 1])
    assert report["atom_indices"].tolist() == [1, 2]
    assert report["bond_indices"].tolist() == [0, 1, 2]
    assert report["bonded_atom_pairs"].tolist() == [[0, 1], [1, 2], [2, 3]]
    assert report["connectivity"]["crossing_bond_indices"].tolist() == [0, 2]
    assert report["explicit_hydrogen_atom_indices"].tolist() == []
    assert report["fields"]["n_explicit_hydrogens"]["values"].tolist() == [2, 0]
    assert "missing_hydrogen_inventory" in report["unassessed_checks"]
    empty = msm.physchem.get_chemical_readiness(chain, selection=[])
    assert empty["bonded_atom_pairs"].shape == (0, 2)
    assert empty["atom_indices"].dtype == np.int64
    assert all(field["status"] == "empty" for field in empty["fields"].values())


def test_ambiguous_state_does_not_silently_use_the_first_state(chain):
    states = chain._chemical_states_domain
    states.append_state()
    states._set_reference_index(None)
    report = msm.physchem.get_chemical_readiness(chain)
    assert report["chemical_state_status"] == "ambiguous"
    assert report["chemical_state_index"] is None
    assert report["fields"]["formal_charge"]["status"] == "missing"
    chosen = msm.physchem.get_chemical_readiness(chain, chemical_state=0)
    assert chosen["fields"]["formal_charge"]["status"] == "present"
    assert states.reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_chemical_readiness(chain, chemical_state=2)


def test_state_and_frame_association_and_nonfinite_coordinates(chain):
    molsys = msm.convert(chain, to_form="molsysmt.MolSys")
    molsys.chemical_states.append_state()
    molsys.chemical_states._states[1].set_atom_attribute("formal_charge", [0, 0, -1, 0])
    molsys.structures.append(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 4, 3)), "nm")
    )
    msm.set(molsys, element="system", structure_chemical_state_index=[0, 1, None])
    xyz = np.zeros((3, 4, 3))
    xyz[1, 2, 0] = np.nan
    molsys.structures.coordinates = msm.pyunitwizard.quantity(xyz, "nm")
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        molsys.structures.coordinates = msm.pyunitwizard.convert(
            molsys.structures.coordinates, to_unit="angstrom"
        )
        report = msm.physchem.get_chemical_readiness(
            molsys, structure_indices=[1, 1], chemical_state="structure"
        )
    assert report["structure_index"] == 1 and report["chemical_state_index"] == 1
    assert report["fields"]["formal_charge"]["values"].tolist() == [0, 0, -1, 0]
    assert report["fields"]["coordinates"]["conflict_indices"].tolist() == [2]
    assert report["fields"]["coordinates"]["unit"] == "nm"
    unknown = msm.physchem.get_chemical_readiness(
        molsys, structure_indices=[2], chemical_state="structure"
    )
    assert unknown["chemical_state_status"] == "unassociated"
    assert unknown["fields"]["formal_charge"]["status"] == "missing"
    with pytest.raises(ArgumentError):
        msm.physchem.get_chemical_readiness(molsys)


def test_standalone_states_and_coordinate_only_forms_are_assessable(chain):
    states = chain._chemical_states_domain
    for source in (states, msm.convert(states, to_form="molsysmt.ChemicalStatesDict")):
        report = msm.physchem.get_chemical_readiness(source)
        assert report["fields"]["atom_type"]["status"] == "missing"
        assert report["fields"]["formal_charge"]["status"] == "present"
    structures = Structures()
    structures.append(coordinates=msm.pyunitwizard.quantity(np.zeros((1, 4, 3)), "nm"))
    for source in (
        structures,
        msm.convert(structures, to_form="molsysmt.StructuresDict"),
        MolSys._from_partial_domains(structures=structures),
    ):
        report = msm.physchem.get_chemical_readiness(source, selection=[3, 1])
        assert report["chemical_state_status"] == "unavailable"
        assert report["fields"]["coordinates"]["values"].tolist() == [True, True]
        assert report["fields"]["formal_charge"]["status"] == "missing"
    unavailable = msm.ChemicalStates(n_atoms=4)
    assert (
        msm.physchem.get_chemical_readiness(unavailable)["chemical_state_status"]
        == "unavailable"
    )


def test_detached_report_and_bounded_connectivity_conflicts(chain):
    chain.atoms.loc[1, "atom_id"] = "a"
    state = chain._chemical_states_domain._states[0]
    state.bonds.loc[0, "atom2_index"] = 0
    report = msm.physchem.get_chemical_readiness(chain)
    assert report["fields"]["atom_id"]["conflict_indices"].tolist() == [0, 1]
    assert report["connectivity"]["invalid_bond_indices"].tolist() == [0]
    report["fields"]["formal_charge"]["values"][0] = 17
    report["bonded_atom_pairs"][:] = -1
    assert state.atom_attributes.formal_charge.tolist() == [0, 0, 0, 0]
    assert state.bonds.atom1_index.tolist() == [0, 1, 2]


def test_rdkit_reference_aromatic_and_virtual_hydrogens_do_not_mutate_source():
    Chem = pytest.importorskip("rdkit.Chem")
    source = Chem.MolFromSmiles("c1ccccc1")
    before = source.ToBinary()
    report = msm.physchem.get_chemical_readiness(source)
    assert (
        report["fields"]["covalent_multiplicity"]["values"].tolist() == ["aromatic"] * 6
    )
    assert report["fields"]["n_implicit_hydrogens"]["values"].tolist() == [1] * 6
    assert report["explicit_hydrogen_atom_indices"].size == 0
    assert source.ToBinary() == before


def test_numeric_and_string_selection_and_single_source_state_agree():
    source = msm.systems["caffeine"]["caffeine.sdf"]
    numeric = msm.physchem.get_chemical_readiness(source, selection=list(range(14, 24)))
    symbolic = msm.physchem.get_chemical_readiness(
        source, selection="atom_type=='H'", chemical_state="structure"
    )
    assert symbolic["chemical_state_status"] == "resolved"
    assert symbolic["chemical_state_index"] == 0
    np.testing.assert_equal(symbolic["fields"], numeric["fields"])


def test_complementary_topology_and_structures_use_shared_atom_axis(chain):
    structures = Structures()
    structures.append(coordinates=msm.pyunitwizard.quantity(np.zeros((1, 4, 3)), "nm"))
    report = msm.physchem.get_chemical_readiness(
        [chain, structures], selection=[2], chemical_state="structure"
    )
    assert report["fields"]["formal_charge"]["values"].tolist() == [0]
    assert report["fields"]["coordinates"]["values"].tolist() == [True]
    assert report["bond_indices"].tolist() == [1, 2]


def test_original_pdbqt_is_inspected_without_discarding_its_tree():
    source = Path(__file__).parents[1] / "form/data/vina_examples/1s63_ligand.pdbqt"
    original = source.read_bytes()
    report = msm.physchem.get_chemical_readiness(source)
    assert report["n_atoms"] == 30
    assert report["connectivity"]["declared_completeness"] == "partial"
    assert report["fields"]["formal_charge"]["status"] == "missing"
    assert report["fields"]["covalent_multiplicity"]["status"] == "missing"
    assert report["fields"]["coordinates"]["status"] == "present"
    assert source.read_bytes() == original


def test_h5msm_queries_one_frame_without_materializing_structures(
    chain, tmp_path, monkeypatch
):
    molsys = msm.convert(chain, to_form="molsysmt.MolSys")
    molsys.structures.append(
        coordinates=msm.pyunitwizard.quantity(np.zeros((7, 4, 3)), "nm")
    )
    output = tmp_path / "source.h5msm"
    msm.convert(molsys, to_form=output)
    from molsysmt.form import _h5msm05_modular

    def reject_full_read(*args, **kwargs):
        raise AssertionError("Readiness must not load the complete structural series.")

    monkeypatch.setattr(
        _h5msm05_modular, "read_independent_structures", reject_full_read
    )
    report = msm.physchem.get_chemical_readiness(
        output, structure_indices=[5], selection=[3, 1]
    )
    assert report["structure_index"] == 5
    assert report["fields"]["formal_charge"]["status"] == "present"
    assert report["fields"]["coordinates"]["status"] == "present"
    assert report["atom_indices"].tolist() == [1, 3]
    with pytest.raises(ArgumentError):
        msm.physchem.get_chemical_readiness(output, structure_indices=[7])


def test_h5msm_preserves_structure_state_association(chain, tmp_path):
    molsys = msm.convert(chain, to_form="molsysmt.MolSys")
    molsys.chemical_states.append_state()
    molsys.chemical_states._states[1].set_atom_attribute("formal_charge", [0, 0, -1, 0])
    molsys.structures.append(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 4, 3)), "nm")
    )
    msm.set(molsys, element="system", structure_chemical_state_index=[0, 1, None])
    output = tmp_path / "states.h5msm"
    msm.convert(molsys, to_form=output)
    report = msm.physchem.get_chemical_readiness(
        output, structure_indices=[1], chemical_state="structure"
    )
    assert report["chemical_state_index"] == 1
    assert report["fields"]["formal_charge"]["values"].tolist() == [0, 0, -1, 0]
    unknown = msm.physchem.get_chemical_readiness(
        output, structure_indices=[2], chemical_state="structure"
    )
    assert unknown["chemical_state_status"] == "unassociated"


def test_h5msm_coordinate_only_and_undeclared_combined_axes(chain, tmp_path):
    import h5py

    structures = Structures()
    structures.append(coordinates=msm.pyunitwizard.quantity(np.zeros((1, 4, 3)), "nm"))
    output = tmp_path / "coordinates.h5msm"
    msm.h5msm.write(MolSys._from_partial_domains(structures=structures), output)
    report = msm.physchem.get_chemical_readiness(output)
    assert report["fields"]["coordinates"]["status"] == "present"
    assert report["chemical_state_status"] == "unavailable"
    molsys = msm.convert([chain, structures], to_form="molsysmt.MolSys")
    combined = tmp_path / "combined.h5msm"
    msm.convert(molsys, to_form=combined)
    with h5py.File(combined, "r+") as file:
        del file["associations"]
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_chemical_readiness(combined)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"selection": [-1]},
        {"selection": [4]},
        {"selection": [True]},
        {"chemical_state": "guess"},
        {"skip_digestion": "yes"},
    ],
)
def test_public_argument_validation(chain, kwargs):
    with pytest.raises(ArgumentError):
        msm.physchem.get_chemical_readiness(chain, **kwargs)


def test_native_readiness_needs_neither_rdkit_nor_ackredit():
    script = """
import importlib.abc
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit', 'ackredit'}:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, Absent())
import molsysmt as msm
report = msm.physchem.get_chemical_readiness(msm.systems['caffeine']['caffeine.sdf'])
assert report['fields']['formal_charge']['status'] == 'present'
assert 'rdkit' not in sys.modules and 'ackredit' not in sys.modules
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
