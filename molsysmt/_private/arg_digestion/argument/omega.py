from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_omega(omega, caller=None):

    if caller in methods_bool_input:
        if isinstance(omega, bool):
            return omega

    raise ArgumentError('omega', value=omega, caller=caller, message=None)

