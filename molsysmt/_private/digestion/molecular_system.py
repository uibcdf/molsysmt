
def digest_single_molecular_system(molecular_system):

    from ..exceptions import MolecularSystemNeededError
    from molsysmt.basic import is_molecular_system

    if is_molecular_system(molecular_system):
        pass
    else:
        raise MolecularSystemNeededError()

def digest_multiple_molecular_systems(molecular_systems):

    from ..exceptions import MultipleMolecularSystemsNeededError
    from molsysmt.basic import are_multiple_molecular_systems

    if are_multiple_molecular_systems(molecular_systems):
        pass
    else:
        raise MultipleMolecularSystemsNeededError()
