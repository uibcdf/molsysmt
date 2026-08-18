from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest()
def get_chain_id(molecular_system, element='atom', selection='all',
                 redefine_indices=False, redefine_ids=False,
                 syntax='MolSysMT', skip_digestion=False):
    """
    Getting chain identifier strings from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='atom'
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
        List of chain IDs.


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
            if redefine_ids:
                from .get_chain_index import get_chain_index
                chain_indices = get_chain_index(
                    molecular_system,
                    element=element,
                    selection=selection,
                    syntax=syntax,
                    redefine_indices=redefine_indices,
                    skip_digestion=True,
                )
                output = chain_indices
            else:
                from molsysmt import get
                output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                             chain_id=True, skip_digestion=True)
        elif redefine_ids:
            from .get_chain_index import get_chain_index
            chain_indices = get_chain_index(molecular_system, element=element, selection=selection, syntax=syntax,
                                            redefine_indices=redefine_indices, skip_digestion=True)
            chain_ids = chain_indices

            if element == 'chain':
                return chain_ids
            else:
                raise NotImplementedError
        else:
            from molsysmt import get
            output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                         chain_id=True, skip_digestion=True)

    elif redefine_ids:

        from .get_chain_index import get_chain_index

        chain_indices = get_chain_index(molecular_system, element=element, selection=selection, syntax=syntax,
                                        redefine_indices=redefine_indices, skip_digestion=True)

        chain_ids = chain_indices

        if element=='chain':

            return chain_ids

        else:

            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_id=True, skip_digestion=True)

    if output is not None:
        arr = np.asarray(output)
        if arr.shape == ():
            output = [str(arr.astype(str))]
        else:
            output = arr.astype(str).tolist()

    return output
