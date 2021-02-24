
def digest_molecular_system(molecular_system):

    from molsysmt.molecular_system import MolecularSystem

    if type(molecular_system)==MolecularSystem:
        return molecular_system
    else:
        return MolecularSystem(molecular_system)

