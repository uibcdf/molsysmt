from molsysmt._private.arg_digestion import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np

@arg_digest(form='MDAnalysis.Universe')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.form.molsysmt_Topology.extract import extract as extract_molsysmt_Topology
    from molsysmt._private.variables import is_all

    n_atoms = item.atoms.n_atoms
    n_groups = item.residues.n_residues
    n_chains = item.segments.n_segments

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains)

    # Atoms
    atom_id = [str(atom.id) for atom in item.atoms]
    atom_name = [atom.name for atom in item.atoms]
    atom_type = [atom.type for atom in item.atoms]
    group_index_of_atoms = [atom.resindex for atom in item.atoms]

    tmp_item.atoms.atom_id = atom_id
    tmp_item.atoms.atom_name = atom_name
    tmp_item.atoms.atom_type = atom_type
    tmp_item.atoms.group_index = group_index_of_atoms

    # Groups
    group_id = [str(res.resid) for res in item.residues]
    group_name = [res.resname for res in item.residues]
    group_type = [get_group_type_from_group_name(res.resname) for res in item.residues]
    chain_index_of_groups = [res.segindex for res in item.residues]

    tmp_item.groups.group_id = group_id
    tmp_item.groups.group_name = group_name
    tmp_item.groups.group_type = group_type
    tmp_item.groups.chain_index = chain_index_of_groups

    # Chains
    chain_id = [str(seg.segid) for seg in item.segments]
    chain_name = [str(seg.segid) for seg in item.segments]

    tmp_item.chains.chain_id = chain_id
    tmp_item.chains.chain_name = chain_name

    # Bonds
    if hasattr(item, 'bonds'):
        bonded_atoms = []
        for bond in item.bonds:
            bonded_atoms.append([bond.atoms[0].index, bond.atoms[1].index])
        if len(bonded_atoms) > 0:
            tmp_item.add_bonds(bonded_atoms, skip_digestion=True)

    # Rebuild remaining hierarchy
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
