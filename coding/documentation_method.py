    """method_name(item, target='system', indices=None, selection='all', structure_indices='all', syntax='MDTraj')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any supported form (see: XXX). The object being acted on by the method.

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection on which the action is applied. The selection can be given by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`); or addressing
       the selected atom index or indices (0-based) by means of an integer, or a list, a tuple, or
       numpy array of integers.

    structure_indices: int, list, tuple, np.ndarray or 'all', default='all'
        Frames selection on which the action is applied. The frame index or indices
        (0-based) can be referred by an integer or by a list, tuple or numpy array of integers.

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'residue', 'chain' or
        'system'.

    to_form: str, default='molsysmt.MolSys'
        Any accepted form by MolSysMt for the output object.

    indices: int, list, tuple or np.ndarray, default=None
        The index or the set of indices of targetted entities ('atom', 'residue' or 'chain') this
        method is going to work with. This entity index or indices (0-based) can be given by
        an integer or a list, tuple or numpy array of integers.

    syntax: str, default='MDTraj'
       Syntaxis used to write argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    Todo
    ----

    Warning
    -------

    """

