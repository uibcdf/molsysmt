from molsysmt._private.digestion import digest


@digest()
def get_molecule_id(molecular_system, element='atom', selection='all', redefine_molecules=False,
                    redefine_ids=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_molecules:
        from .get_molecule_index import get_molecule_index
        output = get_molecule_index(molecular_system, element=element, selection=selection,
                                     redefine_components=True, syntax=syntax)
    elif redefine_ids:
        from .get_molecule_index import get_molecule_index
        output = get_molecule_index(molecular_system, element=element, selection=selection,
                                     redefine_components=False, redefine_indices=False, syntax=syntax)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_id=True)

    return output

