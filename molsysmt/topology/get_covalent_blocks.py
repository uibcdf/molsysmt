from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError, ArgumentError
import numpy as np
from networkx import connected_components
from smonitor import signal

@signal(tags=['api', 'topology'])
@arg_digest()
def get_covalent_blocks(molecular_system, selection='all', remove_bonds=None, output_type='sets',
        syntax='MolSysMT'):
    """
    Identifying the sets of atoms that remain covalently connected when bonds are removed.

    The purpose of this function is `remove_bonds`: it answers which atoms would still
    hold together if the given bonds were cut. That is how the groups of atoms rotating
    around a dihedral angle are obtained, for example.

    Called without `remove_bonds` it returns the **components** of the system, since a
    component is by definition a set of atoms mutually connected through covalent bonds.
    In that case it adds nothing to `get(molecular_system, element='component')`, which
    is the ordinary way of asking for them.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any of the :ref:`supported forms <Introduction_Forms>`.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atom selection used to build the bond graph. Atoms outside it are absent from
        every block, so a selection can split a block just as removing a bond does.
    remove_bonds : array-like, optional
        Pairs of atom indices to remove from the bond graph before the blocks are
        computed. The molecular system itself is not modified: the removal is
        hypothetical and affects only this result.
    output_type : {'sets', 'numpy.ndarray'}, default 'sets'
        Output format: a list of sets of atom indices, or an array labeling each atom
        with the index of the block it belongs to.
    syntax : str, default 'MolSysMT'
        Selection syntax for string-based selections.

    Returns
    -------
    numpy.ndarray or list
        Covalent blocks as sets of atom indices, or a 0-based block label per atom.

    Raises
    ------
    NotImplementedMethodError
        If `output_type` is unsupported.

    Notes
    -----
    - Builds a bond graph with `get_bondgraph` and returns its connected components
      after removing the requested bonds.
    - The blocks are not the `component` attribute of the system unless `remove_bonds`
      is `None` and `selection` is `'all'`. With either of them the result describes a
      hypothetical connectivity, not the system's own components.

    See Also
    --------
    :func:`molsysmt.basic.get`
        Retrieving `component_index` and the rest of the system's own attributes.
    :func:`molsysmt.topology.get_covalent_paths`
        Finding paths of covalently bonded atoms matching an ordered pattern.

    .. versionadded:: 1.0.0
    """

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
                raise ArgumentError('remove_bonds', value=remove_bonds, caller='molsysmt.topology.get_covalent_blocks', message="Input argument bonded_atoms with wrong shape")
        elif len(remove_bonds.shape)==2:
            if remove_bonds.shape[1]!=2:
                raise ArgumentError('remove_bonds', value=remove_bonds, caller='molsysmt.topology.get_covalent_blocks', message="Input argument bonded_atoms with wrong shape")
        else:
            raise ArgumentError('remove_bonds', value=remove_bonds, caller='molsysmt.topology.get_covalent_blocks', message="Input argument bonded_atoms with wrong shape")

        for atom_pair in remove_bonds:
            G.remove_edge(atom_pair[0], atom_pair[1])

    components = connected_components(G)

    del(G)

    if output_type=='sets':

        blocks = list(components)

    elif output_type=='numpy.ndarray':

        n_atoms = get(molecular_system, element='system', n_atoms=True)
        blocks = -np.ones([n_atoms], dtype=int)
        component_index = 0
        for component in components:
            blocks[list(component)]=component_index
            component_index += 1

    else:

        raise NotImplementedMethodError(caller='molsysmt.topology.get_covalent_blocks')

    return np.array(blocks)
