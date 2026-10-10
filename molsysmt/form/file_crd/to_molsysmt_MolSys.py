from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:crd")
def to_molsysmt_MolSys(
    item,
    atom_indices="all",
    structure_indices="all",
    get_missing_bonds=False,
    skip_digestion=False,
):
    """
    Converting from file:crd to molsysmt.MolSys.


    Parameters
    ----------
    item : file:crd
        Input CHARMM coordinate file in standard or extended format.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source atom positions to retain. Native topological extraction uses
        sorted atom-index order, including in the combined MolSys output.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices to retain from the single available structure.
        An empty selection returns zero structures.
    get_missing_bonds : bool, default=False
        Retained compatibility argument. This CRD reader does not infer bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    Notes
    -----
    Atom, group and chain IDs are string labels. Positional indices remain
    integers. Metadata conversion does not establish covalent connectivity
    or a complete chemical state. Topology and coordinates are extracted together
    through the native MolSys operation to keep their atom axes aligned.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['POPC']['popc.crd']
    >>> converted = to_molsysmt_MolSys(molsys, atom_indices=[2, 0])
    >>> converted.get_n_atoms()
    2

    .. versionadded:: 1.0.0
    """

    from molsysmt.native.molsys import MolSys

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, skip_digestion=True)

    return tmp_item.extract(
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
