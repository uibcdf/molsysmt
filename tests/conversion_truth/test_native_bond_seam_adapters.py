import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import Topology


def _build_legacy_metadata_molsys():
    builder = msm.MolSysBuilder()
    atom_0 = builder.add_atom(atom_name="C", atom_type="C")
    atom_1 = builder.add_atom(atom_name="N", atom_type="N")
    builder.add_group([atom_0, atom_1], group_name="LIG")
    builder.add_bond(
        atom_0,
        atom_1,
        bond_order="aromatic",
        bond_type="dative",
    )
    return builder.build()


def test_first_party_serializers_normalize_legacy_bond_metadata(tmp_path):
    molsys = _build_legacy_metadata_molsys()

    topology_dict = msm.convert(molsys.topology, to_form="molsysmt.TopologyDict")
    topology_from_dict = msm.convert(topology_dict, to_form="molsysmt.Topology")

    molsys_dict = msm.convert(molsys, to_form="molsysmt.MolSysDict")
    molsys_from_dict = msm.convert(molsys_dict, to_form="molsysmt.MolSys")

    viewer_json = msm.convert(molsys, to_form="molsysmt.ViewerJSON")
    molsys_from_viewer = msm.convert(viewer_json, to_form="molsysmt.MolSys")

    h5msm_filename = tmp_path / "legacy-metadata.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=str(h5msm_filename))
    molsys_from_h5msm = msm.convert(str(h5msm_filename), to_form="molsysmt.MolSys")

    for topology in (
        topology_from_dict,
        molsys_from_dict.topology,
        molsys_from_viewer.topology,
        molsys_from_h5msm.topology,
    ):
        bonds = topology._get_chemical_state_bonds()
        assert bonds["is_aromatic"].tolist() == [True]
        assert bonds["bond_type"].tolist() == ["dative"]


def test_first_party_single_state_consumers_fail_closed_but_h5msm_preserves_inventory(tmp_path):
    topology = Topology(n_atoms=2)
    topology._append_chemical_state_bonds([[0, 1]], orders="1")
    topology._append_chemical_state(state_id="product")
    topology._set_reference_chemical_state_index(None)

    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.get(topology, element="bond", bond_order=True)
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.convert(topology, to_form="molsysmt.TopologyDict")
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.convert(topology, to_form="molsysmt.ViewerJSON")
    filename = tmp_path / "ambiguous.h5msm"
    msm.convert(topology, to_form="file:h5msm", output_filename=str(filename))
    restored = msm.convert(str(filename), to_form="molsysmt.Topology")
    assert len(restored._chemical_states) == 2
    assert restored._reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.get(restored, element="bond", bond_order=True)


@pytest.mark.parametrize(
    ("target_form", "use_molsys"),
    [
        ("networkx.Graph", False),
        ("mdtraj.Topology", False),
        ("openmm.Topology", False),
        ("pytraj.Topology", False),
        ("string:pdb_text", True),
        ("pdbfixer.PDBFixer", True),
    ],
)
def test_endpoint_adapters_fail_closed_without_reference_state(
    rich_molsys, target_form, use_molsys
):
    topology = rich_molsys.topology
    topology._append_chemical_state(state_id="product")
    topology._set_reference_chemical_state_index(None)

    source = rich_molsys if use_molsys else topology
    with pytest.raises(StructuralInconsistencyError, match="ambiguous"):
        msm.convert(source, to_form=target_form)


@pytest.mark.parametrize(
    ("target_form", "use_molsys"),
    [
        ("networkx.Graph", False),
        ("mdtraj.Topology", False),
        ("openmm.Topology", False),
        ("pytraj.Topology", False),
        ("string:pdb_text", True),
        ("pdbfixer.PDBFixer", True),
    ],
)
def test_endpoint_adapters_fail_closed_without_chemical_state(
    rich_molsys, target_form, use_molsys
):
    rich_molsys.topology._clear_chemical_states()

    source = rich_molsys if use_molsys else rich_molsys.topology
    with pytest.raises(StructuralInconsistencyError, match="no chemical state"):
        msm.convert(source, to_form=target_form)


def test_endpoint_adapters_preserve_known_empty_connectivity(rich_molsys):
    rich_molsys.topology._reset_chemical_state_bonds(n_bonds=0)

    graph = msm.convert(rich_molsys.topology, to_form="networkx.Graph")
    mdtraj_topology = msm.convert(rich_molsys.topology, to_form="mdtraj.Topology")
    openmm_topology = msm.convert(rich_molsys.topology, to_form="openmm.Topology")
    pytraj_topology = msm.convert(rich_molsys.topology, to_form="pytraj.Topology")
    pdb_text = msm.convert(rich_molsys, to_form="string:pdb_text")

    assert graph.number_of_edges() == 0
    assert mdtraj_topology.n_bonds == 0
    assert openmm_topology.getNumBonds() == 0
    assert pytraj_topology.bond_indices.shape == (0,)
    assert "CONECT" not in pdb_text


def test_pdbfixer_subset_uses_output_atom_indices(rich_molsys):
    pdbfixer = msm.convert(
        rich_molsys,
        to_form="pdbfixer.PDBFixer",
        selection=[0, 2],
        structure_indices=[0],
    )

    assert pdbfixer.topology.getNumAtoms() == 2
    assert {
        tuple(sorted((bond.atom1.index, bond.atom2.index)))
        for bond in pdbfixer.topology.bonds()
    } == {(0, 1)}


@pytest.mark.parametrize('target_form', ['string:pdb_text', 'file:pdb', 'pdbfixer.PDBFixer'])
def test_pdb_targets_report_unrepresentable_rich_bond_metadata(
    rich_molsys, target_form, tmp_path
):
    target = target_form
    if target_form == 'file:pdb':
        target = str(tmp_path / 'rich.pdb')

    with pytest.raises(msm.NotCompatibleConversionError, match='Strict conversion'):
        msm.convert(rich_molsys, to_form=target, strict=True)

    _, report = msm.convert(
        rich_molsys,
        to_form=target,
        return_report=True,
    )
    affected = {issue.attribute for issue in report.issues}
    assert {'bond_order', 'bond_type'} <= affected
    assert report.outcome == 'lossy'


def test_pdbfixer_reports_known_empty_connectivity_inference(rich_molsys):
    rich_molsys.topology._reset_chemical_state_bonds(n_bonds=0)

    with pytest.raises(msm.NotCompatibleConversionError, match='Strict conversion'):
        msm.convert(rich_molsys, to_form='pdbfixer.PDBFixer', strict=True)

    _, report = msm.convert(
        rich_molsys,
        to_form='pdbfixer.PDBFixer',
        return_report=True,
    )
    assert any(
        issue.attribute == 'bonded_atoms' and issue.kind == 'target_inference'
        for issue in report.issues
    )


def test_first_party_serializers_omit_unavailable_bond_metadata():
    molsys = _build_legacy_metadata_molsys()
    bonds = molsys.topology._get_chemical_state_bonds()
    bonds.drop(
        columns=["is_aromatic", "bond_type", "joins_components"],
        inplace=True,
    )

    topology_dict = msm.convert(molsys.topology, to_form="molsysmt.TopologyDict")
    molsys_dict = msm.convert(molsys, to_form="molsysmt.MolSysDict")
    viewer_json = msm.convert(molsys, to_form="molsysmt.ViewerJSON")

    assert topology_dict.data["bonds"] == [
        {"atom_index_1": 0, "atom_index_2": 1}
    ]
    assert molsys_dict.data["topology"]["bonds"] == [
        {"atom_index_1": 0, "atom_index_2": 1}
    ]
    assert viewer_json.data["bonds"]["order"] == []
    assert viewer_json.data["bonds"]["type"] == []


def test_h5msm_reader_restores_normalized_chemical_state_bonds(rich_molsys, tmp_path):
    filename = tmp_path / "bond-seam-read.h5msm"
    msm.convert(rich_molsys, to_form="file:h5msm", output_filename=str(filename))

    restored = msm.convert(str(filename), to_form="molsysmt.Topology")

    assert restored._get_chemical_state_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == (
        rich_molsys.topology._get_chemical_state_bonds()[
            ["atom1_index", "atom2_index"]
        ].values.tolist()
    )
    restored_orders = restored._get_chemical_state_bonds()["bond_order"].tolist()
    assert restored_orders[0] == 1
    assert pd.isna(restored_orders[1])
