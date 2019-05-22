def setting(item, element='atom', indices=None, ids=None, **kwargs):

    from molmodmt import duplicate as _duplicate
    import numpy as np

    tmp_item = _duplicate(item)
    if indices is not None:
        set_indices = set(indices)
        array_indices = np.array(indices)
    elif ids is not None:
        set_ids = set(ids)
        array_ids = np.array(ids)

    #element puede ser 'atom', 'residue', 'chain', 'trajectory'

    if element=='atom':

        for option in kwargs:
            if option=='residue_name':
                raise NotImplementedError
            else:
                raise NotImplementedError

    elif element=='residue':

        for option in kwargs:
            if option=='residue_name':
                for residue in tmp_item.topology.residues():
                    if residue.index in set_indices:
                        name = kwargs[option][np.where(array_indices == residue.index)[0][0]]
                        residue.name = name
                for bond in tmp_item.topology.bonds():
                    for ii in [0,1]:
                        if bond[ii].residue.index in set_indices:
                            name = kwargs[option][np.where(array_indices == bond[ii].residue.index)[0][0]]
                            bond[ii].residue.name = name
            else:
                raise NotImplementedError


    elif element=='molecule':
        raise NotImplementedError

    elif element=='chain':
        raise NotImplementedError

    elif element=='trajectory':
        raise NotImplementedError

    return tmp_item

