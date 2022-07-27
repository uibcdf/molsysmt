from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_PDBFile(item, atom_indices='all', coordinates=None):

    if check:

        digest_item(item, 'molsysmt.MolSys')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)

    from . import to_string_pdb_text
    from io import StringIO
    from openmm.app import PDBFile

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates)

    tmp_io = StringIO()
    tmp_io.read(string_pdb_text)
    tmp_item = PDBFile.readFile(tmp_io)

    return tmp_item

