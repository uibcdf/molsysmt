from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_rdkit_Mol(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.basic import get
    from rdkit import Chem
    from rdkit.Chem import EditableMol

    # Get data from MolSys
    atom_names, atom_types, bond_pairs = get(item, element='atom', selection=atom_indices,
                                             name=True, type=True, inner_bonded_atom_pairs=True)

    coordinates = get(item, element='atom', selection=atom_indices,
                      structure_indices=structure_indices, coordinates=True)

    # Build absolute-index → local-index (rdkit) mapping.
    # atom_names has one entry per selected atom in selection order (0..N-1 locally).
    # When atom_indices='all', selected_atoms is [0, 1, ..., N-1] (identity mapping).
    # When atom_indices is a subset, selected_atoms are the absolute indices in order.
    if atom_indices == 'all':
        selected_atoms = list(range(len(atom_names)))
    else:
        selected_atoms = [int(i) for i in atom_indices]

    abs_to_local = {abs_idx: local_idx for local_idx, abs_idx in enumerate(selected_atoms)}

    # Create an empty RDKit molecule
    mol = Chem.Mol()
    emol = EditableMol(mol)

    # Add atoms
    for name, symbol in zip(atom_names, atom_types):
        atom = Chem.Atom(symbol if symbol else 'C')
        emol.AddAtom(atom)

    # Add bonds using local indices derived from the abs→local mapping.
    # bond_pairs contains absolute atom indices; both ends must be in the selection.
    seen_bonds = set()
    for pair in bond_pairs:
        local_i = abs_to_local.get(int(pair[0]))
        local_j = abs_to_local.get(int(pair[1]))
        if local_i is None or local_j is None:
            continue
        if local_i == local_j:
            continue  # guard against self-bonds in invalid topology data
        bond = tuple(sorted((local_i, local_j)))
        if bond not in seen_bonds:
            emol.AddBond(bond[0], bond[1], Chem.rdchem.BondType.SINGLE)
            seen_bonds.add(bond)

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
