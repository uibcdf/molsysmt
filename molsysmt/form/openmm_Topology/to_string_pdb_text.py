from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None):

    from io import StringIO
    from openmm.app import PDBFile
    from molsysmt import __version__ as msm_version
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)
    from molsysmt import pyunitwizard as puw

    if not is_all(atom_indices):
        from . import extract
        item = extract(item, atom_indices=atom_indices)

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

def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    return to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates)

