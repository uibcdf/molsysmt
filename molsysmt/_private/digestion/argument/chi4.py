from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_chi4(chi4, caller=None):

    if caller in methods_bool_input:
        if isinstance(chi4, bool):
            return chi4

    raise ArgumentError('chi4', value=chi4, caller=caller, message=None)

