from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:gro")
def to_openmm_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from file:gro to openmm.Topology.


    Parameters
    ----------
    item : molecular system
        Source object or file in the form named by this adapter.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.


    Notes
    -----
    Uses the native single-entry GRO reader and existing bond inference on
    the complete source before atom extraction. Output atom labels and bonds
    follow native sorted source atom order; the first entry's row-vector box
    is retained. This bridge does not infer arbitrary ligand chemistry or
    assign force-field parameters. See the GRO handler guide for reading limits.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys.to_openmm_Topology import (
        to_openmm_Topology as native_to_openmm,
    )

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    # Infer on the complete native source before selecting atoms. The native
    # extraction keeps source topology and coordinate axes aligned.
    native = to_molsysmt_MolSys(item, atom_indices=atom_indices, skip_digestion=True)
    return native_to_openmm(native, skip_digestion=True)
