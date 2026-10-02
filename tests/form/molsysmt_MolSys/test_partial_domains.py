"""Check public attribute and conversion behavior for partial native systems."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures


def test_state_only_molsys_exposes_its_atom_and_chemical_state_domains():
    states = msm.ChemicalStates(n_atoms=3)
    states.append_state()
    system = MolSys._from_partial_domains(chemical_states=states)

    assert msm.has_attribute(system, "n_atoms")
    assert msm.has_attribute(system, "n_chemical_states")
    assert msm.get(system, n_atoms=True, n_chemical_states=True) == [3, 1]
    assert msm.get(system, chemical_state_index=True) == [0]
    assert msm.get(system, chemical_state_id=True) == [None]
    assert msm.get(system, reference_chemical_state_index=True) == 0
    assert system.get(n_atoms=True) == 3
    assert not msm.has_attribute(system, "n_structures", include_none=True)
    assert not msm.has_attribute(system, "atom_name", include_none=True)
    assert msm.get(system, n_structures=True) is None
    assert msm.get(system, element="atom", atom_name=True) is None
    assert msm.get(system, coordinates=True) is None
    assert msm.convert(system, to_form="molsysmt.ChemicalStates").n_atoms == 3
    available = msm.get_attributes(system)
    assert "n_atoms" in available
    assert "n_chemical_states" in available
    assert "atom_name" not in available
    assert "n_structures" not in available


def test_topology_free_molsys_exposes_stored_structures_and_associations():
    states = msm.ChemicalStates(n_atoms=3)
    states.append_state()
    states.append_state()
    frames = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    )
    system = MolSys._from_partial_domains(chemical_states=states, structures=frames)
    system._set_structure_chemical_state_indices([0, 1])

    assert msm.get(system, n_structures=True) == 2
    assert msm.get(system, structure_chemical_state_index=True) == [0, 1]
    coordinates = msm.get(system, structure_indices=[1, 0], coordinates=True)
    assert coordinates.shape == (2, 3, 3)
    assert msm.get(
        system, structure_indices=[1, 0], structure_chemical_state_index=True
    ) == [1, 0]
    assert msm.convert(system, to_form="molsysmt.Structures").n_structures == 2


def test_missing_domain_conversions_fail_before_creating_output(tmp_path):
    system = MolSys._from_partial_domains(chemical_states=msm.ChemicalStates(n_atoms=2))
    with pytest.raises(ValueError, match="no topology domain"):
        msm.convert(system, to_form="molsysmt.Topology")
    with pytest.raises(ValueError, match="no structures domain"):
        msm.convert(system, to_form="molsysmt.Structures")
    with pytest.raises(
        ValueError,
        match="MolSysDict 0.1 requires topology, chemical states, and structures",
    ):
        msm.convert(system, to_form="molsysmt.MolSysDict")

    filename = tmp_path / "state_only.h5msm"
    msm.convert(system, to_form="file:h5msm", output_filename=filename)
    restored = msm.h5msm.read(str(filename))
    assert restored.topology is None
    assert restored.structures is None
    assert restored.chemical_states.n_atoms == 2


def test_explicit_state_selection_fails_clearly_without_a_topology():
    states = msm.ChemicalStates(n_atoms=2)
    states.append_state()
    system = MolSys._from_partial_domains(chemical_states=states)
    with pytest.raises(msm.ArgumentError, match="chemical_state"):
        msm.get(system, chemical_state=0, n_atoms=True)
