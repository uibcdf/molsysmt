from molsysmt._private.argdigest import arg_digest
import numpy as np


@arg_digest()
def get_molecule_id(molecular_system, element='molecule', selection='all', redefine_indices=False,
                    redefine_ids=False, syntax='MolSysMT', skip_digestion=False):
    """
    Getting molecule identifier strings from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='molecule'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_indices : bool, default=False
        Whether to reassign contiguous 0-based indices.
    redefine_ids : bool, default=False
        Whether to assign sequential string identifiers.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of molecule IDs.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology

        topology = None
        if isinstance(molecular_system, Topology):
            topology = molecular_system
        elif isinstance(molecular_system, MolSys):
            topology = molecular_system.topology

        if topology is not None:
            if redefine_indices or redefine_ids:
                from .get_molecule_index import get_molecule_index
                output = get_molecule_index(molecular_system, element=element, selection=selection,
                                            redefine_indices=redefine_indices or redefine_ids, syntax=syntax,
                                            skip_digestion=True)
            else:
                from molsysmt.basic import get
                output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                             molecule_id=True)
        elif redefine_indices:
            from .get_molecule_index import get_molecule_index
            output = get_molecule_index(molecular_system, element=element, selection=selection,
                                         redefine_indices=True, syntax=syntax)
        elif redefine_ids:
            from .get_molecule_index import get_molecule_index
            output = get_molecule_index(molecular_system, element=element, selection=selection,
                                        redefine_indices=False, syntax=syntax)
        else:
            from molsysmt.basic import get
            output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                         molecule_id=True)

    elif redefine_indices:
        from .get_molecule_index import get_molecule_index
        output = get_molecule_index(molecular_system, element=element, selection=selection,
                                     redefine_indices=True, syntax=syntax)
    elif redefine_ids:
        from .get_molecule_index import get_molecule_index
        output = get_molecule_index(molecular_system, element=element, selection=selection,
                                    redefine_indices=False, syntax=syntax)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_id=True)

    if output is not None:
        arr = np.asarray(output)
        if arr.shape == ():
            output = [str(arr.astype(str))]
        else:
            output = arr.astype(str)
        output = output.tolist()

    return output
