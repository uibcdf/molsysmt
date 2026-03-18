from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Molecule')
def to_openff_Topology(item, skip_digestion=False):

    return item.to_topology()
