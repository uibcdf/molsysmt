from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_molecule_name(molecular_system, element='atom', selection='all', redefine_molecules=False,
                       redefine_names=False, syntax='MolSysMT'):

    if redefine_molecules:

        if element == 'atom':
            from molsysmt.basic import get
            n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax, n_atoms=True)
            output = np.full(n_atoms, None, dtype=object).tolist()
        elif element == 'group':
            from molsysmt.basic import get
            n_groups = get(molecular_system, element='group', selection=selection, syntax=syntax, n_groups=True)
            output = np.full(n_groups, None, dtype=object).tolist()
        elif element == 'molecule':
            from .get_n_molecules import get_n_molecules
            n_molecules = get_n_molecules(molecular_system, selection=selection, redefine_molecules=True,
                                            syntax=syntax)
            output = np.full(n_molecules, None, dtype=object).tolist()
        else:
            raise NotImplementedError

    elif redefine_names:

        if element == 'atom':
            from molsysmt.basic import get
            n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax)
            output = np.full(n_atoms, None, dtype=object).tolist()
        elif element == 'group':
            from molsysmt.basic import get
            n_groups = get(molecular_system, element='group', selection=selection, syntax=syntax)
            output = np.full(n_groups, None, dtype=object).tolist()
        elif element == 'molecule':
            from .get_n_molecules import get_n_molecules
            n_molecules = get_n_molecules(molecular_system, selection=selection, redefine_molecules=False,
                                            syntax=syntax)
            output = np.full(n_molecules, None, dtype=object).tolist()
        elif element == 'entity':
            from .get_n_molecules import get_n_molecules
            n_molecules = get_n_molecules(molecular_system, selection=selection, redefine_molecules=False,
                                            syntax=syntax)
            output = np.full(n_molecules, None, dtype=object).tolist()
        else:
            raise NotImplementedError

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_name=True)

    return output
