from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest(form='rdkit.Mol')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt._private.variables import is_all

    n_atoms = item.GetNumAtoms()
    n_bonds = item.GetNumBonds()

    # RDKit doesn't have a rigid chain/residue hierarchy like PDB, 
    # but atoms often have a PDBResidueInfo object.
    
    tmp_item = Topology(n_atoms=n_atoms)

    atom_id = []
    atom_name = []
    atom_type = []
    
    group_id = []
    group_name = []
    
    # We will group by PDBResidueInfo if present, otherwise treat as one group
    for atom in item.GetAtoms():
        atom_id.append(str(atom.GetIdx()))
        
        info = atom.GetPDBResidueInfo()
        if info:
            atom_name.append(info.GetName().strip())
            atom_type.append(atom.GetSymbol())
        else:
            atom_name.append(atom.GetSymbol() + str(atom.GetIdx()))
            atom_type.append(atom.GetSymbol())

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type

    # Bonds
    if n_bonds > 0:
        bonded_atoms = []
        for bond in item.GetBonds():
            bonded_atoms.append([bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()])
        tmp_item.add_bonds(bonded_atoms, skip_digestion=True)

    # Hierarchy rebuilding
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
