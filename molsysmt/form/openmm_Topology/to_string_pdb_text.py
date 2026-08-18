from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='openmm.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from openmm.Topology to string:pdb_text.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.

    .. versionadded:: 1.0.0
    """

    from io import StringIO
    from openmm.app import PDBFile
    from molsysmt import __version__ as msm_version
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)
    from molsysmt import pyunitwizard as puw
    from smonitor.integrations import context_extra, emit_from_catalog
    from molsysmt._private.smonitor import CATALOG

    if not is_all(atom_indices):
        from . import extract
        item = extract(item, atom_indices=atom_indices)

    n_structures = coordinates.shape[0]
    if n_structures>1:
        emit_from_catalog(
            CATALOG['warnings']['AmbiguousStructureWarning'],
            extra=context_extra(
                caller='molsysmt.form.openmm_Topology.to_string_pdb_text',
                operation='convert',
                extra={'count': n_structures},
            ),
        )

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
