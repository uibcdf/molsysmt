from molsysmt._private.argdigest import arg_digest


@arg_digest(form='rdkit.Mol')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from rdkit.Mol to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys, MolecularMechanics
    from .get_mechanical_attributes import _get_partial_charges
    from molsysmt._private.variables import is_all
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)

    partial_charge = _get_partial_charges(item)
    if partial_charge is not None and not is_all(atom_indices):
        partial_charge = partial_charge[atom_indices]
    tmp_item.molecular_mechanics = MolecularMechanics(
        partial_charge=partial_charge,
    )

    return tmp_item
