from ...exceptions import ArgumentError

methods_bool_input = ["molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets",
        "molsysmt.structure.get_dihedral_angles.get_dihedral_angles"]

def digest_psi(psi, caller=None):

    if caller in methods_bool_input:
        if isinstance(psi, bool):
            return psi

    raise ArgumentError('psi', value=psi, caller=caller, message=None)

