"""Exercise one private native entry point across modular domain presence."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    migrate_04_to_05,
    read_molsys_file,
    write_molsys_file,
)
from molsysmt.native import ChemicalStates, MolSys, Structures, Topology


@pytest.mark.parametrize(
    ("has_topology", "has_chemistry", "has_structures"),
    [
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ],
)
def test_generic_molsys_route_preserves_each_domain_combination(
    tmp_path, has_topology, has_chemistry, has_structures
):
    topology = Topology(n_atoms=2) if has_topology else None
    if has_chemistry:
        states = (
            topology._chemical_states_domain
            if topology is not None
            else ChemicalStates(n_atoms=2)
        )
        if states.n_chemical_states == 0:
            states.append_state()
    else:
        states = None
        if topology is not None:
            topology._clear_chemical_states()
    structures = (
        Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm"))
        if has_structures
        else None
    )
    source = MolSys._from_partial_domains(
        topology=topology, chemical_states=states, structures=structures
    )
    if has_chemistry and has_structures:
        source._set_structure_chemical_state_indices([0, 0])

    filename = tmp_path / "domains.h5msm"
    write_molsys_file(filename, source)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert ("topology" in file) == has_topology
        assert ("chemical_states" in file) == has_chemistry
        assert ("structures" in file) == has_structures

    observed = read_molsys_file(filename)
    assert (observed.topology is not None) == has_topology
    assert (observed.chemical_states is not None) == has_chemistry
    assert (observed.structures is not None) == has_structures
    assert observed.get_n_atoms() == 2
    if has_chemistry and has_topology:
        assert observed.chemical_states is observed.topology._chemical_states_domain
    if has_chemistry and has_structures:
        assert observed._get_structure_chemical_state_indices().tolist() == [0, 0]


def test_generic_reader_rejects_old_schema_instead_of_misreading_it(tmp_path):
    filename = tmp_path / "old.h5msm"
    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.4"
    with pytest.raises(ValueError, match="Expected an H5MSM 0.5"):
        read_molsys_file(filename)


def test_04_migration_keeps_chemical_states_and_frame_values(tmp_path):
    source = MolSys(n_atoms=2)
    source.topology.add_bonds([[0, 1]])
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(12).reshape(2, 2, 3) / 10, "nm"
        ),
        time=msm.pyunitwizard.quantity([0.0, 2.0], "ps"),
    )
    legacy = tmp_path / "legacy.h5msm"
    modern = tmp_path / "modern.h5msm"
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    to_file_h5msm(source, output_filename=str(legacy))

    migrate_04_to_05(legacy, modern)
    with h5py.File(legacy, "r") as file:
        assert file.attrs["version"] == "0.4"
    with h5py.File(modern, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert file.attrs["migrated_from_version"] == "0.4"
        assert set(file) >= {"topology", "chemical_states", "structures"}
    observed = read_molsys_file(modern)
    assert observed.get_n_atoms() == 2
    assert observed.chemical_states.n_chemical_states == 1
    assert len(observed.chemical_states.get_bonds()) == 1
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed.structures.coordinates, to_unit="nm"),
        np.arange(12).reshape(2, 2, 3) / 10,
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed.structures.time, to_unit="ps"),
        [0.0, 2.0],
    )


def test_04_migration_rejects_same_path_and_ambiguous_empty_scaffold(tmp_path):
    filename = tmp_path / "empty04.h5msm"
    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.4"
        file.create_group("topology").attrs["n_atoms"] = 0
        file.create_group("structures")
    with pytest.raises(ValueError, match="distinct source"):
        migrate_04_to_05(filename, filename)
    output = tmp_path / "output.h5msm"
    with pytest.raises(ValueError, match="ambiguous layer presence"):
        migrate_04_to_05(filename, output)
    assert not output.exists()
