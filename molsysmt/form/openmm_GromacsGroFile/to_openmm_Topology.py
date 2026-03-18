from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    # openmm.GromacsGroFile does not expose a full Topology object and does not
    # store the file path, so conversion to openmm.Topology is not supported.
    raise NotImplementedMethodError()
