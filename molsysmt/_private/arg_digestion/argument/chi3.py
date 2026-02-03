from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_chi3(chi3, caller=None):

    if caller in methods_bool_input:
        if isinstance(chi3, bool):
            return chi3

    raise ArgumentError('chi3', value=chi3, caller=caller, message=None)

