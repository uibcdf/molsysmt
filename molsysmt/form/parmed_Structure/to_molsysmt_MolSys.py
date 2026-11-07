from molsysmt._private.argdigest import arg_digest


@arg_digest(form="parmed.Structure")
def to_molsysmt_MolSys(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from parmed.Structure to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        ParmEd structure supplying explicit elements, chemistry, optional
        coordinate structures/cells and available mechanical atom assignments.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Native domains with element symbols in Topology and force-field labels
        and partial charges in MolecularMechanics. Unassigned provider charge
        defaults do not create known zero charges. Mixed assignments retain
        None in the existing nullable mechanics column. Box-only objects retain
        their structure axis without invented coordinates.


    .. versionadded:: 1.0.0
    """

    from molsysmt._private.variables import is_all

    # Match the canonical native topology order across every source domain.
    if not is_all(atom_indices):
        atom_indices = sorted(atom_indices)

    import numpy as np

    from molsysmt.native import MolecularMechanics

    from ._mechanical import assigned_partial_charges
    from ._read_native import read_native
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = read_native(item, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, skip_digestion=True)
    partial_charge = assigned_partial_charges(item)
    ff_types = [
        None if atom.type in {None, ""} else str(atom.type) for atom in item.atoms
    ]
    tmp_item.molecular_mechanics = MolecularMechanics(
        partial_charge=None
        if all(value is None for value in partial_charge)
        else np.asarray(partial_charge, dtype=object),
        atom_ff_type=None if all(value is None for value in ff_types) else ff_types,
    )

    if not is_all(atom_indices) or not is_all(structure_indices):
        from molsysmt.form.molsysmt_MolSys.extract import extract

        tmp_item = extract(
            tmp_item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )

    return tmp_item
