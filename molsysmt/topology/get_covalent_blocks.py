from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
import numpy as np
from networkx import connected_components

@digest()
def get_covalent_blocks(molecular_system, selection='all', remove_bonds=None, output='sets',
        syntax='MolSysMT'):

    from molsysmt.basic import get
    from . import get_bondgraph

    G = get_bondgraph(molecular_system, nodes_name='atom_index', selection=selection, syntax=syntax)

    if remove_bonds is not None:

        if type(remove_bonds) in [list,tuple]:
            remove_bonds = np.array(remove_bonds)

        if len(remove_bonds.shape)==1:
            if remove_bonds.shape[0]==2:
                remove_bonds=remove_bonds.reshape([1,2])
            else:
                raise ValueError("Input argument bonded_atoms with wrong shape")
        elif len(remove_bonds.shape)==2:
            if remove_bonds.shape[1]!=2:
                raise ValueError("Input argument bonded_atoms with wrong shape")
        else:
            raise ValueError("Input argument bonded_atoms with wrong shape")

        for atom_pair in remove_bonds:
            G.remove_edge(atom_pair[0], atom_pair[1])

    components = connected_components(G)

    del(G)

    if output=='sets':

        blocks = list(components)

    elif output=='numpy.ndarray':

        n_atoms = get(molecular_system, element='system', n_atoms=True)
        blocks = -np.ones([n_atoms], dtype=int)
        component_index = 0
        for component in components:
            blocks[list(component)]=component_index
            component_index += 1

    else:

        raise NotImplementedMethodError

    return np.array(blocks)

