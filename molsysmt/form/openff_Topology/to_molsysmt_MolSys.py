from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openff.Topology")
def to_molsysmt_MolSys(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from openff.Topology to molsysmt.MolSys.


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

    from molsysmt._private.variables import is_all

    # Match the canonical native topology order across every source domain.
    if not is_all(atom_indices):
        atom_indices = sorted(atom_indices)

    from molsysmt._private.variables import is_all
    from molsysmt.native import MolecularMechanics

    from ._read_native import read_native
    from .get_mechanical_attributes import _partial_charges
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = read_native(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    partial_charge = _partial_charges(item)
    if partial_charge is not None and not is_all(atom_indices):
        partial_charge = partial_charge[atom_indices]
    tmp_item.molecular_mechanics = MolecularMechanics(partial_charge=partial_charge)
    return tmp_item
