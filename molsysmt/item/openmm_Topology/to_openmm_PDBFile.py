from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_Topology import is_openmm_Topology

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

    from . import to_string_pdb_text
    from io import StringIO
    from openmm.app import PDBFile

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    tmp_io = StringIO()
    tmp_io.read(string_pdb_text)
    tmp_item = PDBFile.readFile(tmp_io)

    return tmp_item

