from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from io import StringIO
    from openmm.app.pdbfile import PDBFile
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFile(tmp_item)

    return tmp_item

