from molsysmt._private.smonitor import ArgumentError


def digest_discard_torsion_tree(discard_torsion_tree, caller=None):
    if isinstance(discard_torsion_tree, bool):
        return discard_torsion_tree
    raise ArgumentError('discard_torsion_tree', value=discard_torsion_tree, caller=caller)
