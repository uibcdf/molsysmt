from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest()
def get_disulfide_bonds(
    molecular_system,
    selection="all",
    structure_index=0,
    max_bond_length=None,
    group_names=None,
    pbc=True,
    syntax="MolSysMT",
    engine="MolSysMT",
    sorted=True,
    skip_digestion=False,
):
    """
    Identifying candidate disulfide bonds between sulfur atoms.

    This build-oriented compatibility function returns S–S pairs inferred from
    group identity and distance in one structure. A candidate is not proof of a
    covalent bond in the topology.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_index : object, default=0
        Argument structure_index.
    max_bond_length : object, default=None
        Argument max_bond_length.
    group_names : object, default=None
        Argument group_names.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Argument engine.
    sorted : bool, default=True
        Whether to sort the returned bonded atom pairs.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of [int, int]
        Candidate atom-index pairs in the selected structure.


    Raises
    ------
    NotSupportedFormError
        If the molecular system format is not supported.

    ArgumentError
        If input values do not meet required conditions.


    Notes
    -----
    - Sulfur atoms are identified based on element type and filtered by group name (e.g., `'CYS'`).
    - The default group name is ``CYS``. Other eligible names may be supplied.
    - Distance units are internally standardized to nanometers.
    - The per-structure detector and its measured distances are available from
      :func:`molsysmt.interactions.disulfides.get_disulfide_candidates`.


    See Also
    --------
    :meth:`molsysmt.Topology.add_bonds`
        Add identified bonds directly to a native topology.

    :func:`molsysmt.structure.get_neighbors`
        Find neighboring atoms within a distance or bond limit.

    :func:`molsysmt.build.get_missing_bonds`
        Automatically infer missing covalent bonds.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.build.get_disulfide_bonds import get_disulfide_bonds
    >>> molsys = msm.convert('5XJH')
    >>> s_s_pairs = get_disulfide_bonds(molsys, max_bond_length='2.15 angstroms')
    >>> len(s_s_pairs)
    2


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Build > Get disulfide bonds <Tutorial_Get_disulfide_bonds>`

    .. versionadded:: 1.0.0
    """

    if engine != "MolSysMT":
        raise NotImplementedMethodError(caller="molsysmt.build.get_disulfide_bonds")

    from molsysmt.interactions.disulfides.get_disulfide_candidates import (
        get_disulfide_candidates,
    )

    pairs_by_structure, _ = get_disulfide_candidates(
        molecular_system,
        selection=selection,
        structure_indices=structure_index,
        max_bond_length=max_bond_length,
        group_names=group_names,
        pbc=pbc,
        syntax=syntax,
        sorted=sorted,
        skip_digestion=True,
    )
    return pairs_by_structure[0].tolist()
