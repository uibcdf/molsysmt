from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.GromacsGroFile")
@dep_digest("openmm")
def to_molsysmt_MolSys(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from openmm.GromacsGroFile to molsysmt.MolSys.


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
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    Notes
    -----
    Applies native atom extraction once after assembling source topology and
    selected-structure geometry. Atom labels and coordinates therefore follow
    the same sorted source atom axis, while structure order and repetitions
    retain their requested meaning with matching periodic boxes. This does
    not add source attributes unavailable from the OpenMM reader, assign
    partial charges or prepare chemistry. The source object is unchanged.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native.molsys import MolSys

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    # Native topology extraction sorts source atom indices. Apply that same
    # extraction once to the assembled system so its coordinates stay aligned.
    return tmp_item.extract(
        atom_indices=atom_indices, copy_if_all=False, skip_digestion=True
    )
