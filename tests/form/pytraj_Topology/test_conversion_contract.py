import molsysmt as msm
from molsysmt.form.molsysmt_Topology.to_pytraj_Topology import (
    _pytraj_chain_id,
    _pytraj_uses_text_chain_id,
)


def _edge_set(bond_pairs):
    return {tuple(sorted((int(atom1), int(atom2)))) for atom1, atom2 in bond_pairs}


def test_native_chain_identifier_is_text_for_pytraj(builder_pdb_molsys):
    topology = builder_pdb_molsys.topology

    assert _pytraj_chain_id(topology, 0) == str(topology.chains.iloc[0]['chain_id'])
    assert _pytraj_chain_id(topology, None) == ''
    assert _pytraj_chain_id(topology, topology.n_chains) == ''


def test_pytraj_chain_identifier_abi_is_detected():
    class TextResidue:
        def __init__(self, name, *, resid, icode, chainID):
            if not isinstance(chainID, str):
                raise AttributeError('chainID must support encode')

    class LegacyResidue:
        def __init__(self, name, *, resid, icode, chainID):
            if not isinstance(chainID, int):
                raise TypeError('an integer is required')

    assert _pytraj_uses_text_chain_id(TextResidue)
    assert not _pytraj_uses_text_chain_id(LegacyResidue)


def test_native_pytraj_roundtrip_preserves_representable_subset(builder_pdb_molsys):
    source = builder_pdb_molsys.topology

    pytraj_topology = msm.convert(source, to_form='pytraj.Topology')
    output = msm.convert(pytraj_topology, to_form='molsysmt.Topology')

    source_bonds = source._get_chemical_state_bonds()[
        ['atom1_index', 'atom2_index']
    ].to_numpy()
    output_bonds = output._get_chemical_state_bonds()[
        ['atom1_index', 'atom2_index']
    ].to_numpy()

    assert output.n_atoms == source.n_atoms
    assert output.n_groups == source.n_groups
    assert output.atoms['atom_name'].tolist() == source.atoms['atom_name'].tolist()
    assert output.atoms['atom_type'].tolist() == source.atoms['atom_type'].tolist()
    assert output.groups['group_name'].tolist() == source.groups['group_name'].tolist()
    assert _edge_set(output_bonds) == _edge_set(source_bonds)
    assert output.n_chains == 0


def test_native_to_pytraj_subset_remaps_bonds(builder_pdb_molsys):
    pytraj_topology = msm.convert(
        builder_pdb_molsys.topology,
        to_form='pytraj.Topology',
        selection=[0, 1],
    )

    assert pytraj_topology.n_atoms == 2
    assert _edge_set(pytraj_topology.bond_indices) == {(0, 1)}


def test_pytraj_to_native_subset_remaps_bonds(builder_pdb_molsys):
    pytraj_topology = msm.convert(
        builder_pdb_molsys.topology,
        to_form='pytraj.Topology',
    )
    output = msm.convert(
        pytraj_topology,
        to_form='molsysmt.Topology',
        selection=[0, 1],
    )

    assert output.n_atoms == 2
    assert _edge_set(
        output._get_chemical_state_bonds()[
            ['atom1_index', 'atom2_index']
        ].to_numpy()
    ) == {(0, 1)}


def test_pytraj_get_uses_native_topology_pipe(builder_pdb_molsys):
    pytraj_topology = msm.convert(
        builder_pdb_molsys.topology,
        to_form='pytraj.Topology',
    )

    atom_names, bonded_atoms = msm.get(
        pytraj_topology,
        element='atom',
        atom_name=True,
        bonded_atoms=True,
    )

    assert atom_names == builder_pdb_molsys.topology.atoms['atom_name'].tolist()
    assert bonded_atoms == [[1], [0, 2], [1], []]
