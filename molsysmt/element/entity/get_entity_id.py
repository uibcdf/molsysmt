from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest()
def get_entity_id(molecular_system, element='entity', selection='all', redefine_indices=False,
                     redefine_ids=False, syntax='MolSysMT', skip_digestion=False):
    """
    Getting entity identifier strings from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='entity'
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
        List of entity IDs.


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
                from .get_entity_index import get_entity_index
                output = get_entity_index(molecular_system, element=element, selection=selection,
                                          redefine_indices=redefine_indices or redefine_ids, syntax=syntax)
            else:
                from molsysmt.basic import get
                output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                             entity_id=True)
        elif redefine_indices:
            from .get_entity_index import get_entity_index
            output = get_entity_index(molecular_system, element=element, selection=selection,
                                      redefine_indices=redefine_indices, syntax=syntax)
        elif redefine_ids:
            from .get_entity_index import get_entity_index
            output = get_entity_index(molecular_system, element=element, selection=selection,
                                      redefine_indices=False, syntax=syntax)
        else:
            from molsysmt.basic import get
            output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                         entity_id=True)

    elif redefine_indices:
        from .get_entity_index import get_entity_index
        output = get_entity_index(molecular_system, element=element, selection=selection,
                                  redefine_indices=redefine_indices, syntax=syntax)
    elif redefine_ids:
        from .get_entity_index import get_entity_index
        output = get_entity_index(molecular_system, element=element, selection=selection,
                                  redefine_indices=False, syntax=syntax)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_id=True)

    if output is not None:
        arr = np.asarray(output)
        if arr.shape == ():
            output = [str(arr.astype(str))]
        else:
            output = arr.astype(str)
        output = output.tolist()

    return output
