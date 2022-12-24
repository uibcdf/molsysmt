from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_PDBFile(item, atom_indices='all', coordinates=None, digest=True):

    from . import to_string_pdb_text
    from io import StringIO
    from openmm.app import PDBFile

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, digest=False)

    tmp_io = StringIO()
    tmp_io.read(string_pdb_text)
    tmp_item = PDBFile.readFile(tmp_io)

    return tmp_item

