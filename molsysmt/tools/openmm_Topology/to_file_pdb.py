from molsysmt.tools.pdbfixer_PDBFixer.is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongCoordinatesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_coordinates

def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

    from molsysmt.tools.openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    string_pdb_text = openmm_Topology_to_string_pdb_text(item, atom_indices=atom_indices, coordinates=None, check=False)

    with open(output_filename, 'w') as file:
        file.write(string_pdb_text)
    tmp_item = output_filename

    return tmp_item

