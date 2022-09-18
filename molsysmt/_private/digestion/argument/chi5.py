from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_chi5(chi5, caller=None):

    if caller in methods_bool_input:
        if isinstance(chi5, bool):
            return chi5

    raise ArgumentError('chi5', value=chi5, caller=caller, message=None)

