from molsysmt.molecular_system import MolecularSystem

def digest_molecular_system(molecular_system):

    if type(molecular_system)==MolecularSystem:
        return molecular_system
    else:
        return MolecularSystem(molecular_system)

