from molsysmt._private.arg_digestion import arg_digest


@arg_digest()
def get_n_molecules(molecular_system, selection='all', redefine_molecules=False,
                     syntax='MolSysMT'):

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from .get_molecule_index import get_molecule_index

        if isinstance(molecular_system, Topology):
            return len(molecular_system.molecules.index) if not redefine_molecules else len(
                get_molecule_index(
                    molecular_system, element='molecule', selection='all', redefine_indices=True, syntax=syntax
                )
            )
        if isinstance(molecular_system, MolSys):
            return len(molecular_system.topology.molecules.index) if not redefine_molecules else len(
                get_molecule_index(
                    molecular_system, element='molecule', selection='all', redefine_indices=True, syntax=syntax
                )
            )

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
