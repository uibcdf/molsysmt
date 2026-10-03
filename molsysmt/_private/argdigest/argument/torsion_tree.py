from molsysmt._private.smonitor import ArgumentError


def digest_torsion_tree(torsion_tree, caller=None):
    if torsion_tree is None or isinstance(torsion_tree, dict):
        return torsion_tree
    raise ArgumentError('torsion_tree', value=torsion_tree, caller=caller)
