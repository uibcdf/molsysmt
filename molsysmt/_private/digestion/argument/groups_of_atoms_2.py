from ...exceptions import ArgumentError

def digest_groups_of_atoms_2(groups_of_atoms_2, caller=None):

    if groups_of_atoms_2 is None:
        return None

    from .groups_of_atoms import digest_groups_of_atoms

    try:
        return digest_groups_of_atoms(groups_of_atoms_2, caller=caller)
    except:
        raise ArgumentError('groups_of_atoms_2', value=groups_of_atoms_2, caller=caller, message=None)

