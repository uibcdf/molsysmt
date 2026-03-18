from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Topology')
def to_openmm_Topology(item, skip_digestion=False):

    return item.to_openmm()
