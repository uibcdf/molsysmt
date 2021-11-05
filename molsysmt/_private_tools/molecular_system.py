from .lists_and_tuples import is_list_or_tuple

def digest_molecular_system(molecular_system):

    from molsysmt.native.molecular_system import MolecularSystem

    if type(molecular_system)==MolecularSystem:
        return molecular_system
    elif is_list_or_tuple(molecular_system):
        if len(molecular_system)==1:
            if type(molecular_system[0])==MolecularSystem:
                return molecular_system[0]
            else:
                return MolecularSystem(molecular_system[0])
        else:
            return MolecularSystem(molecular_system)
    else:
        return MolecularSystem(molecular_system)

