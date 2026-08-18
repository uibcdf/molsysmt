from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.GromacsGroFile to openmm.Topology.

    Parameters
    ----------
    item : openmm.GromacsGroFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    # openmm.GromacsGroFile does not expose a full Topology object and does not
    # store the file path, so conversion to openmm.Topology is not supported.
    raise NotImplementedMethodError()
