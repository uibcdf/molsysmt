from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.GromacsGroFile to openmm.Topology.

    Parameters
    ----------
    item : openmm.GromacsGroFile
        Source item in openmm.GromacsGroFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    # openmm.GromacsGroFile does not expose a full Topology object and does not
    # store the file path, so conversion to openmm.Topology is not supported.
    raise NotImplementedMethodError()
