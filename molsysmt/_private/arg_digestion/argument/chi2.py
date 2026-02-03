from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_chi2(chi2, caller=None):

    if caller in methods_bool_input:
        if isinstance(chi2, bool):
            return chi2

    raise ArgumentError('chi2', value=chi2, caller=caller, message=None)

