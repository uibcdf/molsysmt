"""Testing direct metadata access for CHARMM CRD files."""

import numpy as np
import pytest

import molsysmt as msm


def test_get_n_atoms_reads_the_crd_header():
    crd = msm.systems["POPC"]["popc.crd"]

    assert msm.get(crd, element="system", n_atoms=True) == 134


@pytest.fixture(params=[False, True], ids=["standard", "extended"])
def crd_file(tmp_path, request):
    path = tmp_path / "small.crd"
    atoms = [
        (23, 10, "ALA", "CA", 1.0, 2.0, 3.0, "A", "10", 0.0),
        (41, 10, "ALA", "N", 4.0, 5.0, 6.0, "A", "10", 0.0),
        (77, 20, "GLY", "CA", 7.0, 8.0, 9.0, "B", "20", 0.0),
    ]
    if request.param:
        header = f"{len(atoms):10d}  EXT\n"
        pattern = "{:10d}{:10d}  {:8s}  {:8s}{:20.10f}{:20.10f}{:20.10f}  {:8s}  {:8s}{:20.10f}\n"
    else:
        header = f"{len(atoms):5d}\n"
        pattern = "{:5d}{:5d} {:4s} {:4s}{:10.5f}{:10.5f}{:10.5f} {:4s} {:4s}{:10.5f}\n"
    path.write_text(
        "* analytical coordinates\n*\n"
        + header
        + "".join(pattern.format(*atom) for atom in atoms)
    )
    return str(path)


@pytest.mark.parametrize(
    "attribute, expected",
    [
        ("atom_index", [2, 0, 2]),
        ("atom_id", ["77", "23", "77"]),
        ("atom_name", ["CA", "CA", "CA"]),
        ("atom_type", ["C", "C", "C"]),
        ("group_index", [1, 0, 1]),
        ("group_id", ["20", "10", "20"]),
        ("group_name", ["GLY", "ALA", "GLY"]),
        ("group_type", ["amino acid", "amino acid", "amino acid"]),
    ],
)
def test_metadata_preserves_source_atom_positions(crd_file, attribute, expected):
    result = msm.get(crd_file, element="atom", selection=[2, 0, 2], **{attribute: True})
    assert list(result) == expected


def test_group_count_and_labels(crd_file):
    assert msm.get(crd_file, n_groups=True) == 2
    indices, ids, names = msm.get(
        crd_file, element="group", group_index=True, group_id=True, group_name=True
    )
    assert list(indices) == [0, 1]
    assert list(ids) == ["10", "20"]
    assert list(names) == ["ALA", "GLY"]


def test_native_conversion_keeps_string_ids(crd_file):
    topology = msm.convert(crd_file, to_form="molsysmt.Topology")
    for table, column, expected in [
        (topology.atoms, "atom_id", ["23", "41", "77"]),
        (topology.groups, "group_id", ["10", "20"]),
        (topology.chains, "chain_id", ["0", "1"]),
    ]:
        assert table[column].tolist() == expected
        assert all(isinstance(value, str) for value in table[column])


def test_metadata_and_coordinates_remain_aligned(crd_file):
    result = msm.get(
        crd_file,
        element="atom",
        selection=[2, 0, 2],
        atom_id=True,
        coordinates=True,
        output_type="dictionary",
    )
    assert list(result["atom_id"]) == ["77", "23", "77"]
    coordinates = msm.pyunitwizard.get_value(result["coordinates"], to_unit="nm")
    assert coordinates.shape == (1, 3, 3)
    np.testing.assert_allclose(
        coordinates, [[[0.7, 0.8, 0.9], [0.1, 0.2, 0.3], [0.7, 0.8, 0.9]]]
    )


@pytest.mark.parametrize(
    "to_form", ["molsysmt.Topology", "molsysmt.Structures", "molsysmt.MolSys"]
)
def test_conversion_honors_atom_subset(crd_file, to_form):
    subset = msm.convert(crd_file, to_form=to_form, selection=[2, 0])
    assert msm.get(subset, n_atoms=True) == 2
    if to_form != "molsysmt.Structures":
        assert list(msm.get(subset, element="atom", atom_id=True)) == ["23", "77"]
    if to_form != "molsysmt.Topology":
        coordinates = msm.pyunitwizard.get_value(
            msm.get(subset, coordinates=True), to_unit="nm"
        )
        expected = (
            [[[0.7, 0.8, 0.9], [0.1, 0.2, 0.3]]]
            if to_form == "molsysmt.Structures"
            else [[[0.1, 0.2, 0.3], [0.7, 0.8, 0.9]]]
        )
        np.testing.assert_allclose(coordinates, expected)


@pytest.mark.parametrize("to_form", ["molsysmt.Structures", "molsysmt.MolSys"])
def test_conversion_can_select_zero_structures(crd_file, to_form):
    subset = msm.convert(crd_file, to_form=to_form, structure_indices=[])
    assert msm.get(subset, n_structures=True) == 0


@pytest.mark.parametrize(
    "selection, expected", [("all", [0, 1, 2]), ([], []), ([2, 0, 2], [2, 0, 2])]
)
def test_atom_indices_need_only_the_header(crd_file, monkeypatch, selection, expected):
    from importlib import import_module

    adapter = import_module("molsysmt.form.file_crd")

    def reject_topology(*args, **kwargs):
        raise AssertionError("A positional-only query must not construct topology.")

    monkeypatch.setattr(adapter, "to_molsysmt_Topology", reject_topology, raising=False)
    assert (
        msm.get(crd_file, element="atom", selection=selection, atom_index=True)
        == expected
    )
    assert adapter.get_atom_index_from_atom(crd_file, indices=None) is None


@pytest.mark.parametrize(
    "to_form", ["molsysmt.Topology", "molsysmt.Structures", "molsysmt.MolSys"]
)
def test_conversion_can_select_zero_atoms(crd_file, to_form):
    subset = msm.convert(crd_file, to_form=to_form, selection=[])
    assert msm.get(subset, n_atoms=True) == 0
    if to_form != "molsysmt.Topology":
        assert msm.get(subset, coordinates=True).shape == (1, 0, 3)


def test_selected_coordinates_respect_nondefault_unit_policy(crd_file):
    puw = msm.pyunitwizard
    original_units = puw.configure.get_standard_units()
    with puw.context(standard_units=["angstrom", "fs", "degree"]):
        molsys = msm.convert(crd_file, selection=[2, 0], to_form="molsysmt.MolSys")
        coordinates = msm.get(molsys, coordinates=True)
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="nm"),
            [[[0.1, 0.2, 0.3], [0.7, 0.8, 0.9]]],
        )
        assert puw.get_unit(coordinates) == puw.get_unit(puw.quantity(1.0, "angstrom"))
    assert puw.configure.get_standard_units() == original_units
