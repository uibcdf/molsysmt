from molsysmt._private.digestion import arg_digest
from molsysmt.dependencies import requires

@arg_digest(form='string:pdb_id')
@requires('pdbfixer')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from pdbfixer import PDBFixer

    from ..pdbfixer_PDBFixer import extract

    pdb_id = item
    
    if pdb_id.startswith('pdb_id:'):
        pdb_id = pdb_id.replace('pdb_id','')

    tmp_item = PDBFixer(pdbid=pdb_id)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)

    return tmp_item

