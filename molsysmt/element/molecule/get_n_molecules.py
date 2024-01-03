from molsysmt._private.digestion import digest


@digest()
def get_n_molecules(molecular_system, selection='all', redefine_molecules=False,
                     syntax='MolSysMT'):

    if redefine_molecules:

        from .get_molecule_index import get_molecule_index

        aux = get_molecule_index(molecular_system, element='molecule', selection=selection,
                                  redefine_indices=True, syntax=syntax)

        output = len(aux)

        del aux

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                     n_molecules=True)

    return output

