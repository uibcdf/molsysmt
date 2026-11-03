from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Topology")
def to_molsysmt_MolSys(
    item,
    atom_indices="all",
    coordinates=None,
    box=None,
    skip_digestion=False,
    *,
    get_missing_bonds=True,
):
    """
    Converting from openmm.Topology to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    get_missing_bonds : bool, default=True
        Infer available intra-group template bonds when the source has no edges.
        False retains its explicitly empty graph. This argument is keyword-only.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    Notes
    -----
    Existing edges retain explicit evidence. Empty-source inference uses the
    constructed native domains without converting the source recursively.
    OpenMM Topology supplies no coordinates: inferred candidates use templates,
    not distances, peptide geometry or disulfide detection. Inferred connectivity
    remains partial; unsupported groups do not acquire guessed edges.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from openmm.app import Topology, element
    >>> source = Topology()
    >>> group = source.addResidue('HOH', source.addChain('W'))
    >>> _ = [source.addAtom(name, atom_type, group) for name, atom_type in
    ...      [('O', element.oxygen), ('H1', element.hydrogen), ('H2', element.hydrogen)]]
    >>> molsys = msm.convert(source, to_form='molsysmt.MolSys', get_missing_bonds=False)
    >>> molsys.get(n_atoms=True, n_bonds=True)
    [3, 0]

    .. admonition:: User guide

       See :ref:`Tutorial_Convert` for source projections and optional inference.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native.structures import Structures

    from . import get_box_from_system
    from ._read_native import read_native

    tmp_item = read_native(
        item,
        atom_indices=atom_indices,
        get_missing_bonds=get_missing_bonds,
        skip_digestion=True,
    )
    tmp_item.structures = Structures()
    if box is None:
        box = get_box_from_system(item)
    tmp_item.structures.append(coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item
