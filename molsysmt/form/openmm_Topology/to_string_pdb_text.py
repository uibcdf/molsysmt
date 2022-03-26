from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_Topology import is_openmm_Topology

def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, check=True):

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

    from io import StringIO
    from openmm.app import PDBFile
    from molsysmt import __version__ as msm_version
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)
    from molsysmt import puw

    n_structures = coordinates.shape[0]
    if n_structures>1:
        import warnings
        warnings.warn("Openmm.Topology/to_string_pdb_text got more than a single structure. Only the 0-th is taken.")

    tmp_io = StringIO()
    coordinates = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    PDBFile.writeFile(item, coordinates, tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    tmp_item = filedata

    return tmp_item

