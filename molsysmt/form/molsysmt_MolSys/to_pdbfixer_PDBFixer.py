from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    try:
        from pdbfixer.pdbfixer import PDBFixer
    except:
        raise LibraryNotFoundError('pdbfixer')

    from . import to_string_pdb_text
    from io import StringIO

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    if item.topology.bonds.shape[0]>0:

        bonds_before = item.topology.bonds[['atom1_index', 'atom2_index']].to_numpy().tolist()

        bonds_after = []
        for ii in tmp_item.topology.bonds():
            if ii.atom1.index<ii.atom2.index:
                bonds_after.append([ii.atom1.index, ii.atom2.index])
            else:
                bonds_after.append([ii.atom2.index, ii.atom1.index])

        missing_bonds = set([tuple(ii) for ii in bonds_before]) - set([tuple(ii) for ii in bonds_after])

        if len(missing_bonds):

            atoms_list = list(tmp_item.topology.atoms())

            for atom1_index, atom2_index in missing_bonds:
                tmp_item.topology.addBond(atoms_list[atom1_index], atoms_list[atom2_index])

    return tmp_item

