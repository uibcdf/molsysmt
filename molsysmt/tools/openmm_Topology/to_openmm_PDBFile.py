from molsysmt.tools.openmm_Topology.is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongCoordinatesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.coordinates import digest_coordinates

def to_openmm_PDBFile(item, atom_indices='all', coordinates=None, check=True):

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
    from io import StringIO
    from openmm.app import PDBFile

    string_pdb_text = openmm_Topology_to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    tmp_io = StringIO()
    tmp_io.read(string_pdb_text)
    tmp_item = PDBFile.readFile(tmp_io)

    return tmp_item

