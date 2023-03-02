from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None):

    from . import to_string_pdb_text

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates)

    with open(output_filename, 'w') as file:
        file.write(string_pdb_text)
    tmp_item = output_filename

    return tmp_item

def _to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    return to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates)

