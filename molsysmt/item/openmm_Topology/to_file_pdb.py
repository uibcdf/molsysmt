from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None):

    if check:

        digest_item(item, 'openmm.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)

    from . import to_string_pdb_text

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates)

    with open(output_filename, 'w') as file:
        file.write(string_pdb_text)
    tmp_item = output_filename

    return tmp_item

