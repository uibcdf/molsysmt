from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def to_molsysmt_Structures(
    item,
    atom_indices="all",
    structure_indices="all",
    discard_properties=False,
    skip_digestion=False,
    *,
    stereo_engine=None,
):
    """Converting a single SDF record into native coordinates.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF input file; coordinates are declared in angstroms.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include; only index zero exists.
    discard_properties : bool, default=False
        Explicitly authorize discarding SD property blocks without native storage.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    stereo_engine : str or None, default=None
        Keyword-only optional 'rdkit' provider for explicit stereo interpretation.
        None retains native dependency-free parsing and rejects stereo flags.

    Returns
    -------
    molsysmt.Structures
        Coordinates converted through PyUnitWizard to native nanometers.

    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        discard_properties=discard_properties,
        stereo_engine=stereo_engine,
        skip_digestion=True,
    ).structures
