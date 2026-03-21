from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_rdkit_Mol(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.basic import get
    from rdkit import Chem
    from rdkit.Chem import EditableMol
    import numpy as np

    # Get data from MolSys
    atom_names, atom_types, bonded_atoms = get(item, element='atom', selection=atom_indices, 
                                               name=True, type=True, inner_bonded_atoms=True)
    
    coordinates = get(item, element='atom', selection=atom_indices, 
                      structure_indices=structure_indices, coordinates=True)

    # Create an empty RDKit molecule
    mol = Chem.Mol()
    emol = EditableMol(mol)

    # Add atoms
    for name, symbol in zip(atom_names, atom_types):
        atom = Chem.Atom(symbol if symbol else 'C')
        # We can store the name in PDBResidueInfo later if needed
        emol.AddAtom(atom)

    # Add bonds (handling unique pairs)
    seen_bonds = set()
    for i, neighbors in enumerate(bonded_atoms):
        for j in neighbors:
            pair = tuple(sorted((i, j)))
            if pair not in seen_bonds:
                emol.AddBond(int(pair[0]), int(pair[1]), Chem.rdchem.BondType.SINGLE)
                seen_bonds.add(pair)

    mol = emol.GetMol()

    # Add coordinates as Conformers
    if coordinates is not None:
        import pyunitwizard as puw
        coords_val = puw.get_value(coordinates, to_unit='angstroms')
        
        for i in range(coords_val.shape[0]):
            conf = Chem.Conformer(mol.GetNumAtoms())
            for j in range(mol.GetNumAtoms()):
                conf.SetAtomPosition(j, coords_val[i, j, :])
            mol.AddConformer(conf, assignId=True)

    return mol
