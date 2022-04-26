_item_fullname_=None

def is_molsysmt_MolecularMechanicsDict(item):

    output = False

    if type(item) is dict:

        from molsysmt.native.molecular_mechanics_dict import molecular_mechanics_parameters

        keys = set(item.keys())
        output = (keys <= molecular_mechanics_parameters)

    return output

