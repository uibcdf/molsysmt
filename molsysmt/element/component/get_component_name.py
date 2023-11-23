from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_component_name(molecular_system, element='atom', selection='all', redefine_components=False,
                       redefine_names=False, syntax='MolSysMT'):

    if redefine_components:

        if element == 'atom':
            from molsysmt.basic import get
            n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax, n_atoms=True)
            output = np.full(n_atoms, None, dtype=object).tolist()
        elif element == 'group':
            from molsysmt.basic import get
            n_groups = get(molecular_system, element='group', selection=selection, syntax=syntax, n_groups=True)
            output = np.full(n_groups, None, dtype=object).tolist()
        elif element == 'component':
            from .get_n_components import get_n_components
            n_components = get_n_components(molecular_system, selection=selection, redefine_components=True,
                                            syntax=syntax)
            output = np.full(n_components, None, dtype=object).tolist()
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
        elif element == 'component':
            from .get_n_components import get_n_components
            n_components = get_n_components(molecular_system, selection=selection, redefine_components=False,
                                            syntax=syntax)
            output = np.full(n_components, None, dtype=object).tolist()
        else:
            raise NotImplementedError

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_name=True)

    return output
