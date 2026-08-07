from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:pdb_id')
@dep_digest('pdbfixer')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from pdbfixer import PDBFixer

    from ..pdbfixer_PDBFixer.extract import extract

    from molsysmt.form.string_pdb_id import _extract_pdb_id
    tmp_item = PDBFixer(pdbid=_extract_pdb_id(item))
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)

    return tmp_item

