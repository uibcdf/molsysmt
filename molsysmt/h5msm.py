"""Reading versioned H5MSM domains and selecting explicit output schemas."""

import h5py

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.h5msm_storage.versions import DEFAULT_WRITE_VERSION

__all__ = [
    "read",
    "write",
    "read_layers",
    "read_axis_sizes",
    "write_layers",
    "append_structures",
    "migrate_04_to_05",
    "migrate_to_05",
]


@arg_digest()
def read(filename, skip_digestion=False):
    """Reading an H5MSM file as a native molecular system.

    Parameters
    ----------
    filename : str
        Path to an H5MSM 0.3, 0.4, 0.5, experimental 0.6, or 1.0 file.
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
    Reading 0.3 or 0.4 emits a warning with a source-preserving conversion.
    Writing uses 1.0. An H5MSM 0.5
    file containing named interactions can be read as a partial MolSys even
    without topology, chemical states, or structures. Topology, chemical states
    and named analyses can also coexist without Structures when their shared
    axes have declared identity links. Coordinates and chemical-state assignments
    to structures are not inferred. A present-empty
    interaction layer has no index domains and requires :func:`read_layers`.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.h5msm_storage.modular import read_molsys_file

    with h5py.File(filename, "r") as file:
        version = file.attrs.get("version")
    if isinstance(version, bytes):
        version = version.decode()
    if version in {"0.3", "0.4"}:
        from molsysmt.basic import convert

        return convert(filename, to_form="molsysmt.MolSys")
    return read_molsys_file(filename)


@arg_digest()
def write(
    molecular_system,
    output_filename,
    skip_digestion=False,
    *,
    format_version=DEFAULT_WRITE_VERSION,
):
    """Writing a native molecular system in an explicitly selected H5MSM schema.

    Parameters
    ----------
    molecular_system : molsysmt.MolSys
        Native molecular system to serialize.
    output_filename : str or pathlib.Path
        Path for a new H5MSM file.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    format_version : str, default='1.0'
        Output schema. '1.0' stores the independent native domains, including
        molecular mechanics. '0.5' selects the mechanics-free schema and
        '0.6' selects the experimental modular schema.

    Returns
    -------
    str or pathlib.Path
        Path of the written file.

    Raises
    ------
    ValueError
        If the native system contains data that the 0.5 codec cannot encode
        without loss. Nonempty molecular-mechanics data are rejected because
        H5MSM 0.5 has no mechanics layer. Stored assignment reports and
        present-empty reports or tables also count as mechanics data.

    Notes
    -----
    Topology, chemical states and named interactions can be written without
    Structures. The writer records identity links for the native system's shared
    atom and structure axes. H5MSM 0.6 and 1.0 preserve typed mechanical
    values and original assignment reports without recalculation. New 0.6 and 1.0 files
    are published atomically without replacing an existing destination; the
    destination filesystem must support hard links. This is atomic visibility,
    not crash durability. Analysis coverage, source maps and original producer
    versions are retained; absent coordinates and periodic boxes stay absent.

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
    ...     _ = msm.h5msm.write(molsys, path, format_version="1.0")
    ...     msm.h5msm.read(path).get_n_atoms()
    2

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.h5msm_storage.versions import write_version

    version = write_version(format_version)
    if version != "0.5":
        from molsysmt._private.h5msm_storage.modular import write_molsys_file

        write_molsys_file(output_filename, molecular_system, format_version=version)
    else:
        from molsysmt.form._h5msm05_modular import write_molsys_file

        write_molsys_file(output_filename, molecular_system)
    return output_filename


@arg_digest()
def read_layers(filename, layers=None, analysis_names=None, skip_digestion=False):
    """Reading selected optional H5MSM modular layers independently.

    Parameters
    ----------
    filename : str
        Path to an H5MSM 0.5, experimental 0.6, or 1.0 file.
    layers : str or iterable of str, default=None
        Layer names to read; None reads the layers defined by the stored root.
        Molecular mechanics is available in 0.6 and 1.0. An explicit request
        for it in 0.5 returns None for that layer.
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
    from molsysmt._private.h5msm_storage.versions import root_version
    from molsysmt.form._h5msm05_modular import read_modular_file

    with h5py.File(filename, "r") as file:
        version = root_version(file)
    names = {layers} if isinstance(layers, str) else set(layers or ())
    if version != "0.5" or "molecular_mechanics" in names:
        from molsysmt._private.h5msm_storage.modular import read_modular_file
    return read_modular_file(filename, layers=layers, analysis_names=analysis_names)


@arg_digest()
def read_axis_sizes(filename, skip_digestion=False):
    """Reading declared modular index-space cardinalities without payload arrays.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to an H5MSM 0.5, experimental 0.6, or 1.0 file.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    dict
        Endpoint tuples (layer, analysis_name, axis) mapped to integer sizes.
        analysis_name is None except for named interactions. Axes are 'atom',
        'structure' and chemical 'state'. Absent or unknown axes are omitted.

    Raises
    ------
    ValueError
        If the root version or declared cardinalities are unsupported.

    Notes
    -----
    This reads schema metadata, not domain arrays or complete layer validation.
    Equal sizes do not establish correspondence; inspect declared associations
    separately with read_layers. A mechanics-only layer retains its explicit atom
    count here even when its native parameter-only object has no atom table.

    Examples
    --------
    >>> import tempfile
    >>> from pathlib import Path
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolecularMechanics
    >>> with tempfile.TemporaryDirectory() as directory:
    ...     path = Path(directory) / "mechanics.h5msm"
    ...     _ = msm.h5msm.write_layers(path, molecular_mechanics=MolecularMechanics(),
    ...         mechanics_n_atoms=7, format_version="0.6")
    ...     msm.h5msm.read_axis_sizes(path)
    {('molecular_mechanics', None, 'atom'): 7}

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.h5msm_storage.modular import read_axis_sizes as read_sizes

    return read_sizes(filename)


@arg_digest()
def write_layers(
    output_filename,
    *,
    topology=None,
    chemical_states=None,
    structures=None,
    molecular_mechanics=None,
    mechanics_n_atoms=None,
    format_version=DEFAULT_WRITE_VERSION,
    interactions=None,
    associations=None,
    skip_digestion=False,
):
    """Writing independently owned H5MSM modular domain layers.

    Parameters
    ----------
    output_filename : str or pathlib.Path
        Path for a new H5MSM file.
    topology : molsysmt.Topology, default=None
        Stable atom inventory and hierarchy.
    chemical_states : molsysmt.ChemicalStates, default=None
        State-dependent chemical information.
    structures : molsysmt.Structures, default=None
        Structure-aligned series, with coordinates in nanometers.
    molecular_mechanics : molsysmt.MolecularMechanics or none, default=None
        Stored model requests, atom parameters and detached assignment reports.
        Requires format_version='0.6' or '1.0'; no calculation or rebinding occurs.
    mechanics_n_atoms : int or none, default=None
        Explicit atom count of the mechanical layer, required when it is supplied.
        Equal counts do not declare correspondence with another domain.
    format_version : str, default='1.0'
        Output schema. '1.0' is the default modular root. '0.5' selects the
        mechanics-free root and '0.6' selects the experimental mechanics root.
    interactions : dict, default=None
        Named sparse interaction analyses.
    associations : list of dict, default=None
        Explicit index-space links between the provided layers. Identity maps
        require equal source and target cardinalities and index-for-index
        correspondence. A prefix into a larger target remains an explicit map;
        structure and chemical-state populations need not have equal lengths.
    skip_digestion : bool, default=False
        Whether to skip argument validation for a trusted internal call.

    Returns
    -------
    str or pathlib.Path
        Path of the written file.

    Notes
    -----
    An explicit 0.5 target rejects a supplied mechanics layer. Reading declared axis sizes
    validates metadata cardinalities, not chemical identity or full payloads.
    Storage does not parameterize or execute a mechanical model.

    Examples
    --------
    >>> import tempfile
    >>> from pathlib import Path
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolecularMechanics
    >>> with tempfile.TemporaryDirectory() as directory:
    ...     path = Path(directory) / "mechanics.h5msm"
    ...     _ = msm.h5msm.write_layers(path,
    ...         molecular_mechanics=MolecularMechanics(forcefield="request"),
    ...         mechanics_n_atoms=7, format_version="0.6")
    ...     msm.h5msm.read_axis_sizes(path)
    {('molecular_mechanics', None, 'atom'): 7}

    .. admonition:: User guide

       See :ref:`user-tools-form-h5msm-06` for experimental stored mechanics.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.h5msm_storage.versions import write_version
    from molsysmt.form._h5msm05_modular import write_modular_file

    version = write_version(format_version)
    options = {}
    if version != "0.5":
        from molsysmt._private.h5msm_storage.modular import write_modular_file

        options = dict(
            molecular_mechanics=molecular_mechanics,
            mechanics_n_atoms=mechanics_n_atoms,
            format_version=version,
        )
    elif molecular_mechanics is not None or mechanics_n_atoms is not None:
        raise ValueError(
            "H5MSM 0.5 has no molecular mechanics layer; explicitly request format_version='1.0' or '0.6'."
        )
    write_modular_file(
        output_filename,
        topology=topology,
        chemical_states=chemical_states,
        structures=structures,
        interactions=interactions,
        associations=associations,
        **options,
    )
    return output_filename


@arg_digest()
def append_structures(
    filename,
    structures,
    *,
    structure_state_indices=None,
    block_size=256,
    skip_digestion=False,
):
    """Appending complete structures to a topology-free modular H5MSM file.

    Parameters
    ----------
    filename : str
        Path to the H5MSM 0.5, experimental 0.6, or 1.0 file to extend.
    structures : molsysmt.Structures
        Complete structure rows matching the stored series and atom axis.
    structure_state_indices : list of int, default=None
        Chemical-state indices for the appended structures when the file has an
        explicit structure-to-state link; -1 denotes an unknown state.
    block_size : int, default=256
        Maximum number of structure rows written in one block.
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
    from molsysmt._private.h5msm_storage.versions import (
        MECHANICS_VERSIONS,
        root_version,
    )
    from molsysmt.form._h5msm05_modular import append_modular_structures

    with h5py.File(filename, "r") as file:
        version = root_version(file)
    options = {}
    if version in MECHANICS_VERSIONS:
        from molsysmt._private.h5msm_storage.modular import _DOMAINS

        options = dict(expected_version=version, layers=_DOMAINS)
    append_modular_structures(
        filename,
        structures,
        structure_state_indices=structure_state_indices,
        block_size=block_size,
        **options,
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
