    """into(item, target='system', indices=None, selection='all', frame_indices='all', syntaxis='MDTraj')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolModMT. (See: XXX)

    target: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'residue', 'chain' or
        'system'.

    to_form: str, default='molmodmt.MolMod'
        Any accepted form by MolModMt for the output object.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of targetted entities ('atom', 'residue' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntaxis parsable by MolModMT (see: :func:`molmodmt.select`).

    syntaxis: str, default='MDTraj'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolModMt can be found in section XXX (see: :func:`molmodmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the target
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molmodmt.get`, :func:`molmodmt.select`
    Notes
    -----

    Todo
    ----

    Warning
    -------

    """

