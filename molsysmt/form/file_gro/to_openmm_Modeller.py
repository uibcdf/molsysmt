from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:gro")
def to_openmm_Modeller(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from file:gro to openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Source object or file in the form named by this adapter.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    Notes
    -----
    Uses native GRO conversion and its single-entry reading scope. Atom
    extraction occurs before provider construction, keeping coordinates and
    topology in the same native sorted source order. Modeller holds the first
    selected structure and its box; repeated selection does not create a
    coordinate ensemble in Modeller. Bond inference uses the existing native
    policy, without chemical preparation or new force-field assignments.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys.to_openmm_Modeller import (
        to_openmm_Modeller as native_to_openmm,
    )

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    native = to_molsysmt_MolSys(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return native_to_openmm(native, skip_digestion=True)
