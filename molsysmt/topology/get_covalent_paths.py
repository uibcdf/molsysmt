from molsysmt._private.argdigest import arg_digest
from smonitor import signal
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt.basic import select

@signal(tags=['api', 'topology'])
@arg_digest()
def get_covalent_paths(molecular_system, path=None, selection='all', syntax='MolSysMT'):
    """
    Finding paths of covalently bonded atoms matching an ordered pattern.

    Every returned path is a walk along covalent bonds whose n-th atom satisfies the
    n-th selection of `path`. Typical uses are locating the atom quartets that define
    a dihedral angle, or the donor-hydrogen pairs of a hydrogen bond.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any of the :ref:`supported forms <Introduction_Forms>`.
    path : list of selections
        Ordered pattern. Position *n* is a selection listing the atoms allowed at step
        *n* of the walk, so `len(path)` is the length of every returned path.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Global atom filter applied before the walk.
    syntax : str, default 'MolSysMT'
        Selection syntax for string-based selections.

    Returns
    -------
    numpy.ndarray
        Array of shape `(n_paths, len(path))` with the atom indices of every path found.
        Order within a path follows the pattern; paths are not deduplicated by reversal.

    Notes
    -----
    - "Path" is used in the graph sense: a walk over the covalent bond graph. It is
      unrelated to the `chain` element of a molecular system, which is a polymer chain.
      To work with those, use :func:`molsysmt.basic.get` with `element='chain'`.
    - Only covalent bonds are traversed. See :func:`molsysmt.topology.get_bondgraph`
      for the graph itself.

    See Also
    --------
    :func:`molsysmt.topology.get_covalent_blocks`
        Sets of atoms mutually connected through covalent bonds, optionally after
        removing bonds.

    .. versionadded:: 1.0.0
    """

    from . import get_bondgraph

    if is_all(selection):
        mask = None
    else:
        mask = select(molecular_system, selection=selection, syntax=syntax)

    path_atom_indices = []

    for sel_in_path in path:
        atom_indices = select(molecular_system, selection=sel_in_path, mask=mask)
        path_atom_indices.append(atom_indices)

    atom_indices = np.sort(np.unique(np.concatenate(path_atom_indices)))

    graph = get_bondgraph(molecular_system, selection=atom_indices, nodes_name='atom_index')

    n_positions = len(path_atom_indices)

    output = [[ii] for ii in path_atom_indices[0]]
    for position in range(n_positions):
        path_atom_indices[position] = set(path_atom_indices[position])

    for position in range(1, n_positions):
        previous_position = position-1
        tmp_output=output.copy()
        output=[]
        for walk in tmp_output:
            for ii in graph.neighbors(walk[previous_position]):
                if ii in path_atom_indices[position]:
                    new_walk = walk.copy()
                    new_walk.append(ii)
                    output.append(new_walk)
    del(graph)

    return np.array(output, dtype=int)
