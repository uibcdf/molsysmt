from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    try:
        from pdbfixer import PDBFixer
    except:
        raise LibraryNotFoundError('pdbfixer')

    from ..pdbfixer_PDBFixer import extract

    pdb_id = item
    
    if pdb_id.startswith('pdb_id:'):
        pdb_id = pdb_id.replace('pdb_id','')

    tmp_item = PDBFixer(pdbid=pdb_id)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

def _to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices)

