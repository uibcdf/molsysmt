from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_chi1(chi1, caller=None):

    if caller in methods_bool_input:
        if isinstance(chi1, bool):
            return chi1

    raise ArgumentError('chi1', value=chi1, caller=caller, message=None)

