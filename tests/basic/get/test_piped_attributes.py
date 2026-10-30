import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt.basic.get import _piped_molecular_system
from molsysmt.form import _dict_modules


def test_piped_molecular_system_for_nglview_topological_attributes():
    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.pdb"],
        to_form="molsysmt.MolSys",
    )
    view = msm.convert(molsys, to_form="nglview.NGLWidget")

    piped_systems, piped_attributes = _piped_molecular_system(
        view,
        "atom",
        ["atom_index", "group_index", "entity_index"],
    )

    assert len(piped_systems) == 1
    assert msm.get_form(piped_systems[0]) == "molsysmt.Topology"
    assert piped_attributes == [["atom_index", "group_index", "entity_index"]]


def test_piped_molecular_system_for_nglview_mixed_attributes():
    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.pdb"],
        to_form="molsysmt.MolSys",
    )
    view = msm.convert(molsys, to_form="nglview.NGLWidget")

    piped_systems, piped_attributes = _piped_molecular_system(
        view,
        "atom",
        ["atom_index", "coordinates"],
    )

    assert len(piped_systems) == 1
    assert msm.get_form(piped_systems[0]) == "molsysmt.MolSys"
    assert piped_attributes == [["atom_index", "coordinates"]]


def test_get_mixed_attributes_from_topology_and_trajectory_composite():
    topology = msm.systems["chicken villin HP35"][
        "traj_chicken_villin_HP35_solvated.h5msm"
    ]
    trajectory = msm.systems["chicken villin HP35"][
        "traj_chicken_villin_HP35_solvated.dcd"
    ]

    names, coordinates = msm.get(
        [topology, trajectory],
        selection=[0, 1, 2, 3, 4],
        atom_name=True,
        coordinates=True,
    )

    assert len(names) == 5
    assert np.shape(coordinates) == (20, 5, 3)


def test_single_attribute_uses_direct_getter_when_available(t4_pdb_file):
    piped_systems, piped_attributes = _piped_molecular_system(
        t4_pdb_file,
        "system",
        ["n_atoms"],
    )

    assert piped_systems is None
    assert piped_attributes is None


@pytest.mark.parametrize("fixture_name", ["hp35_bcif_file", "hp35_bcif_gz_file"])
def test_get_bonded_atom_pairs_from_bcif_public_api(fixture_name, request):
    molecular_system = request.getfixturevalue(fixture_name)

    bonded_atom_pairs = msm.get(str(molecular_system), bonded_atom_pairs=True)

    assert np.shape(bonded_atom_pairs) == (602, 2)


def test_single_attribute_uses_pipe_when_direct_getter_is_missing(t4_pdb_file):
    piped_systems, piped_attributes = _piped_molecular_system(
        t4_pdb_file,
        "atom",
        ["atom_type"],
    )

    assert len(piped_systems) == 1
    assert msm.get_form(piped_systems[0]) == "molsysmt.MolSys"
    assert piped_attributes == [["atom_type"]]


def test_declared_attribute_without_getter_or_pipe_raises_molsysmt_exception(
    t4_pdb_molsys,
    monkeypatch,
):
    module = _dict_modules["molsysmt.MolSys"]
    monkeypatch.delattr(module, "get_formal_charge_from_atom")

    with pytest.raises(NotWithThisFormError):
        msm.get(t4_pdb_molsys, element="atom", formal_charge=True)


def test_piped_form_metadata_for_known_bulk_extraction_forms():
    expected_pipes = {
        "nglview.NGLWidget": (
            None,
            "molsysmt.Structures",
            "molsysmt.MolSys",
        ),
        "file:gro": ("molsysmt.MolSys", "molsysmt.Structures", "molsysmt.MolSys"),
        "file:xtc": (None, "mdtraj.XTCTrajectoryFile", None),
        "molsysviewer.MolSysView": (
            "molsysmt.MolSys",
            "molsysmt.MolSys",
            "molsysmt.MolSys",
        ),
        "molsysmt.H5MSMFileHandler": (None, "molsysmt.Structures", None),
        "mmcif.PdbxContainers.DataContainer": (
            "molsysmt.MolSys",
            "molsysmt.Structures",
            "molsysmt.MolSys",
        ),
        "string:pdb_text": (
            "molsysmt.MolSys",
            "molsysmt.Structures",
            "molsysmt.MolSys",
        ),
        "string:pdb_id": (
            "molsysmt.MolSys",
            "molsysmt.Structures",
            "molsysmt.MolSys",
        ),
        "string:alphafold_id": (
            "molsysmt.MolSys",
            "molsysmt.Structures",
            "molsysmt.MolSys",
        ),
    }

    for form, expected in expected_pipes.items():
        module = _dict_modules[form]
        observed = (
            module.piped_topological_attribute,
            module.piped_structural_attribute,
            module.piped_any_attribute,
        )
        assert observed == expected


def test_metadata_pipe_requests_no_coordinate_structures(monkeypatch):
    """Chemical metadata conversion must not copy a trajectory payload."""
    from importlib import import_module

    mda = pytest.importorskip("MDAnalysis")
    source = mda.Universe.empty(2, n_residues=1, atom_resindex=[0, 0], trajectory=True)
    source.add_TopologyAttr("names", ["C1", "O1"])
    source.add_TopologyAttr("types", ["C", "O"])
    source.add_TopologyAttr("elements", ["C", "O"])
    source.add_TopologyAttr("ids", [1, 2])
    source.add_TopologyAttr("resnames", ["LIG"])
    source.add_TopologyAttr("resids", [1])
    source.load_new(np.zeros((5, 2, 3)), order="fac")
    geometry = import_module("molsysmt.form.MDAnalysis_Universe.to_molsysmt_Structures")
    original = geometry.to_molsysmt_Structures
    seen = []

    def bounded(
        item, atom_indices="all", structure_indices="all", skip_digestion=False
    ):
        assert not isinstance(structure_indices, str)
        assert len(structure_indices) == 0
        seen.append(len(structure_indices))
        return original(
            item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=skip_digestion,
        )

    monkeypatch.setattr(geometry, "to_molsysmt_Structures", bounded)
    result = msm.get(source, element="atom", atom_name=True, atom_type=True)
    assert result == [["C1", "O1"], ["C", "O"]]
    assert seen
    assert source.trajectory.n_frames == 5
