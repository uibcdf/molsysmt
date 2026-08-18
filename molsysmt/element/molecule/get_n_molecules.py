from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_n_molecules(molecular_system, selection='all', redefine_molecules=False,
                     syntax='MolSysMT'):
    """
    Getting the total number of molecules in a molecular system or selection.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection filter.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    int
        Number of molecules.

    .. versionadded:: 1.0.0
    """

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
