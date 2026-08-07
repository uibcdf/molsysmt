from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_openmm_Modeller(item, atom_indices='all', skip_digestion=False):

    # openmm.GromacsGroFile does not expose a full Topology object, so
    # conversion to openmm.Modeller is not supported.
    raise NotImplementedMethodError()
