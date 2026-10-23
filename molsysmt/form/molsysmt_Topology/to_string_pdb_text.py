from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
def to_string_pdb_text(
    item, atom_indices="all", coordinates=None, box=None, skip_digestion=False
):
    """
    Converting from molsysmt.Topology to string:pdb_text.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Length quantity with shape (n_structures, n_atoms, 3) on the full source
        atom axis. Atom selection applies jointly to topology and coordinates.
    box : object, default=None
        Optional length quantity containing row-vector periodic cells.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    >>> molsys = msm.convert(source, get_missing_bonds=False)
    >>> text = to_string_pdb_text(molsys.topology,
    ...                           coordinates=molsys.structures.coordinates)
    >>> msm.get_form(text)
    'string:pdb_text'

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys.to_string_pdb_text import (
        to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text,
    )
    from molsysmt.native import MolSys

    tmp_item = MolSys()
    tmp_item.topology = item.copy()
    tmp_item.structures.append(coordinates=coordinates, box=box, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_string_pdb_text(
        tmp_item, atom_indices=atom_indices, skip_digestion=True
    )

    return tmp_item
