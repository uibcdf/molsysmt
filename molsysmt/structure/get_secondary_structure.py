from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
import numpy as np


@signal(tags=['api', 'structure'])
@arg_digest()
def get_secondary_structure(molecular_system, selection='all', structure_indices='all',
                            simplified=True, syntax='MolSysMT', engine='MDTraj'):
    """
    Secondary structure assignment per residue over one or more structures.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Residue (group) selection. Non-protein residues are assigned 'NA'.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    simplified : bool, default True
        If True, use the simplified 3-category DSSP scheme ('H', 'E', 'C').
        If False, use the full 8-category DSSP scheme.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MDTraj'}, default 'MDTraj'
        Backend used for the DSSP computation.

    Returns
    -------
    numpy.ndarray, shape (n_structures, n_groups), dtype 'U2'
        Secondary structure code per residue per structure.

        Simplified codes (``simplified=True``):

        - ``'H'`` : Helix (alpha, 3/10, or pi).
        - ``'E'`` : Strand (extended or isolated beta-bridge).
        - ``'C'`` : Coil (turn, bend, or loop).
        - ``'NA'`` : Non-protein residue.

        Full DSSP codes (``simplified=False``):

        - ``'H'`` : Alpha helix.
        - ``'G'`` : 3/10 helix.
        - ``'I'`` : Pi helix.
        - ``'E'`` : Extended strand.
        - ``'B'`` : Isolated beta-bridge.
        - ``'T'`` : Hydrogen-bonded turn.
        - ``'S'`` : Bend.
        - ``' '`` : Loop or irregular element.
        - ``'NA'`` : Non-protein residue.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    if engine == 'MDTraj':

        from mdtraj import compute_dssp
        from molsysmt.basic import convert, select, get

        tmp_item = convert(molecular_system, to_form='mdtraj.Trajectory',
                           structure_indices=structure_indices)
        assignments = compute_dssp(tmp_item, simplified=simplified)
        # assignments shape: (n_frames, n_residues), dtype bytes or str

        # mdtraj returns bytes (b'H') — decode to str
        if assignments.dtype.kind == 'S':
            assignments = assignments.astype('U2')

        if selection != 'all':
            group_indices = get(molecular_system, element='group', selection=selection,
                                syntax=syntax, group_index=True)
            # group_index returns per-atom list; flatten to unique group indices
            flat = np.unique(np.concatenate(group_indices))
            assignments = assignments[:, flat]

        return assignments

    else:

        raise NotImplementedMethodError()
