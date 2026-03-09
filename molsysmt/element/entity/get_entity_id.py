from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest()
def get_entity_id(molecular_system, element='entity', selection='all', redefine_indices=False,
                     redefine_ids=False, syntax='MolSysMT', skip_digestion=False):

    if selection == 'all':
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
