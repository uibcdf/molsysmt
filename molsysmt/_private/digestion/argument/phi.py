from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_phi(phi, caller=None):

    if caller in methods_bool_input:
        if isinstance(phi, bool):
            return phi

    raise ArgumentError('phi', value=phi, caller=caller, message=None)

