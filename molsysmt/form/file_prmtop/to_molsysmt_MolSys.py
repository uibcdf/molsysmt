from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:prmtop")
def to_molsysmt_MolSys(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from file:prmtop to molsysmt.MolSys.


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

    from molsysmt.form.openmm_Topology._read_native import read_native
    from molsysmt.native import Structures

    from .to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile

    source = to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    output = read_native(
        source.topology, atom_indices=atom_indices, skip_digestion=True
    )
    output.structures = Structures()
    return output
