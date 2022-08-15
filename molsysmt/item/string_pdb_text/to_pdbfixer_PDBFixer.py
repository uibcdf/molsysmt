from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    from io import StringIO
    from pdbfixer.pdbfixer import PDBFixer
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

