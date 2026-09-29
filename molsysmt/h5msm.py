"""Reading legacy H5MSM files and writing the modular 0.5 schema."""

import h5py

from molsysmt._private.argdigest import arg_digest

__all__ = [
    "read", "write", "read_layers", "write_layers", "append_structures",
    "migrate_04_to_05", "migrate_to_05",
]


@arg_digest()
def read(filename, skip_digestion=False):
    """Reading an H5MSM file as a native molecular system.

    Parameters
    ----------
    filename : str
        Path to an H5MSM 0.3, 0.4, or 0.5 file.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    molsysmt.MolSys
        Molecular system with the stored domain presence and associations.

    Raises
    ------
    ValueError
        If the file has an unsupported version or its domains cannot be represented by
        one native molecular system.

    Notes
    -----
    Reading 0.3 or 0.4 emits a warning with the migration helper. Writing uses
    0.5; legacy files remain readable without changing them. An H5MSM 0.5
    file containing named interactions can be read as a partial MolSys even
    without topology, chemical states, or structures. A present-empty
    interaction layer has no index domains and requires :func:`read_layers`.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import read_molsys_file

    with h5py.File(filename, "r") as file:
        version = file.attrs.get("version")
    if isinstance(version, bytes):
        version = version.decode()
    if version in {"0.3", "0.4"}:
        from molsysmt.basic import convert

        return convert(filename, to_form="molsysmt.MolSys")
    return read_molsys_file(filename)


@arg_digest()
def write(molecular_system, output_filename, skip_digestion=False):
    """Writing a native molecular system in the H5MSM 0.5 schema.

    Parameters
    ----------
    molecular_system : molsysmt.MolSys
        Native molecular system to serialize.
    output_filename : str or pathlib.Path
        Path for a new H5MSM 0.5 file.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    str or pathlib.Path
        Path of the written file.

    Raises
    ------
    ValueError
        If the native system contains data that the 0.5 codec cannot encode
        without loss. Nonempty molecular-mechanics data are rejected because
        H5MSM 0.5 has no mechanics layer.

    Examples
    --------
    >>> import tempfile
    >>> from pathlib import Path
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys, Structures
    >>> with tempfile.TemporaryDirectory() as directory:
    ...     molsys = MolSys(n_atoms=2)
    ...     molsys.structures = Structures(
    ...         coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    ...     )
    ...     path = str(Path(directory) / "sample.h5msm")
    ...     _ = msm.h5msm.write(molsys, path)
    ...     msm.h5msm.read(path).get_n_atoms()
    2

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import write_molsys_file

    write_molsys_file(output_filename, molecular_system)
    return output_filename


@arg_digest()
def read_layers(filename, layers=None, analysis_names=None, skip_digestion=False):
    """Reading selected optional H5MSM 0.5 layers independently.

    Parameters
    ----------
    filename : str
        Path to an H5MSM 0.5 file.
    layers : str or iterable of str, default=None
        Layer names to read; None reads every optional layer.
    analysis_names : str or iterable of str, default=None
        Names of interaction analyses to read when interactions are requested.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    dict
        Requested layers keyed by their schema names. An absent layer is None;
        a present but empty interaction layer is an empty dictionary.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import read_modular_file

    return read_modular_file(filename, layers=layers, analysis_names=analysis_names)


@arg_digest()
def write_layers(
    output_filename, *, topology=None, chemical_states=None, structures=None,
    interactions=None, associations=None, skip_digestion=False,
):
    """Writing independently owned H5MSM 0.5 domain layers.

    Parameters
    ----------
    output_filename : str or pathlib.Path
        Path for a new H5MSM 0.5 file.
    topology : molsysmt.Topology, default=None
        Stable atom inventory and hierarchy.
    chemical_states : molsysmt.ChemicalStates, default=None
        State-dependent chemical information.
    structures : molsysmt.Structures, default=None
        Frame-aligned structural series, with coordinates in nanometers.
    interactions : dict, default=None
        Named sparse interaction analyses.
    associations : list of dict, default=None
        Explicit index-space links between the provided layers.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    str or pathlib.Path
        Path of the written file.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import write_modular_file

    write_modular_file(
        output_filename, topology=topology, chemical_states=chemical_states,
        structures=structures, interactions=interactions, associations=associations,
    )
    return output_filename


@arg_digest()
def append_structures(
    filename, structures, *, structure_state_indices=None, block_size=256,
    skip_digestion=False,
):
    """Appending complete frames to a topology-free H5MSM 0.5 file.

    Parameters
    ----------
    filename : str
        Path to the H5MSM 0.5 file to extend.
    structures : molsysmt.Structures
        Complete frame rows matching the stored series and atom axis.
    structure_state_indices : list of int, default=None
        Chemical-state indices for the appended frames when the file has an
        explicit structure-to-state link; -1 denotes an unknown state.
    block_size : int, default=256
        Maximum number of frame rows written in one block.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    str
        Path of the extended file.

    Notes
    -----
    This append path requires no topology or interaction layer. It validates
    input before resizing datasets but is not crash transactional. Stored and
    incoming alternate-location fields must have matching presence; sparse
    site records grow with the structural series when both are present.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import append_modular_structures

    append_modular_structures(
        filename, structures, structure_state_indices=structure_state_indices,
        block_size=block_size,
    )
    return filename


@arg_digest()
def migrate_04_to_05(filename, output_filename, skip_digestion=False):
    """Migrating a complete H5MSM 0.4 file to an H5MSM 0.5 file.

    Parameters
    ----------
    filename : str
        Path to a legacy H5MSM 0.4 file.
    output_filename : str or pathlib.Path
        Path for a new H5MSM 0.5 file. It must differ from filename.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    pathlib.Path
        Path of the migrated file.

    Raises
    ------
    ValueError
        If the source is not 0.4, its empty scaffolding is ambiguous, or a
        source field cannot be encoded by the 0.5 writer.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import migrate_04_to_05 as migrate

    return migrate(filename, output_filename)


@arg_digest()
def migrate_to_05(filename, output_filename, skip_digestion=False):
    """Migrating an H5MSM 0.3 or 0.4 file to the 0.5 schema.

    Parameters
    ----------
    filename : str
        Path to a legacy H5MSM 0.3 or 0.4 file.
    output_filename : str or pathlib.Path
        Path for a new H5MSM 0.5 file. It must differ from filename.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    pathlib.Path
        Path of the migrated file.

    Raises
    ------
    ValueError
        If the source version is unsupported, its empty scaffolding is
        ambiguous, or a source field cannot be encoded by the 0.5 writer.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form._h5msm05_modular import migrate_to_05 as migrate

    return migrate(filename, output_filename)
