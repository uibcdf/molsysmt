"""Reading pose coordinates on a declared source atom axis."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "form"])
@arg_digest(form="file:pdbqt")
def read_poses(
    item,
    molecular_system,
    atom_map,
    structure_indices="all",
    missing_atoms="error",
    return_report=False,
    skip_digestion=False,
):
    """Reading PDBQT poses against a known chemical source and export map.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT file path. A single ligand or a
        balanced MODEL/ENDMDL ensemble is supported.
    molecular_system : molecular system
        Any supported form supplying the original ordered element inventory
        and one complete chemical state used to produce atom_map.
    atom_map : dict
        Completed molsysmt.atom_export@1 PDBQT writer map. JSON-decoded lists
        are accepted. Correspondence is declared, not authenticated.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Pose structure indices (0-based), independent of MODEL labels. Order
        and repetitions are preserved. All poses are validated before selection.
    missing_atoms : str, default='error'
        'error' rejects source atoms omitted by the export; 'omit' explicitly
        returns the retained source subsystem, with no coordinates for absent
        atoms. No missing hydrogen is generated or placed at its parent.
    return_report : bool, default=False
        Return a dictionary with molecular_system and a detached report when
        True. The report contains atom/structure maps and opaque remarks.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    molsysmt.MolSys or dict
        Independent native system with new pose coordinates in nm and known
        source chemistry in sorted retained source-atom order. With a report,
        its schema is molsysmt.pdbqt_pose_read@1. Model labels are string
        structure IDs; an unwrapped ligand has no declared model label.

    Raises
    ------
    ArgumentError
        If an input form, option or structure selection is invalid.
    FormatError
        If model grammar, map binding, atom fields or torsion trees disagree.
    StructuralInconsistencyError
        If the source chemical graph is unavailable or incomplete.

    Notes
    -----
    Positional atom/structure indices require plain integer values; quantity
    wrappers are rejected, including explicit dimensionless quantities.

    This experimental resident reader reuses the bounded AutoDock4 parser.
    It validates serials, names, elements, written charges, available AutoDock
    labels and the exported tree in every pose. It does not infer graph edges,
    spatial correspondence, scores, rankings or missing hydrogen coordinates.
    Source coordinates, boxes, times, observables and interaction analyses are
    not copied. MolecularMechanics is not transferred; written charges and
    labels are recorded in the optional report, without claiming a new charge
    assignment. With missing_atoms='omit', bonds incident on omitted atoms
    disappear through ordinary extraction; virtual-H counts are not increased.
    Use build.merge_nonpolar_hydrogens before export for a chemically prepared
    reduced representation. A source map is not a map through earlier H creation.
    Ordinary convert/get also support homogeneous MODEL ensembles, but retain
    only the chemistry explicitly declared by PDBQT, not the known source graph.

    See Also
    --------
    molsysmt.build.merge_nonpolar_hydrogens : Prepare a typed reduced source.
    molsysmt.basic.convert : Write PDBQT with return_atom_map=True.

    Examples
    --------
    Preparing this example explicitly requires optional RDKit; reading the
    resulting native source and PDBQT needs no chemical engine.

    >>> import numpy as np
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
    >>> molsys = msm.build.assign_autodock_atom_types(molsys, typing_scheme='autodock4')
    >>> molsys = msm.build.assign_partial_charges(molsys, method='gasteiger_marsili')
    >>> n = molsys.get_n_atoms()
    >>> tree = dict(schema_version='molsysmt.pdbqt-torsion-tree@1',
    ...     atom_ids=molsys.topology.atoms.atom_id.to_numpy(),
    ...     fragment_atom_indices=np.arange(n), fragment_offsets=np.array([0, n]),
    ...     branch_atom_pairs=np.empty((0, 2), dtype=int),
    ...     branch_fragment_pairs=np.empty((0, 2), dtype=int),
    ...     root_fragment_index=0, torsdof=0)
    >>> text, atom_map = msm.convert(molsys, to_form='string:pdbqt_text',
    ...     typing_scheme='autodock4', torsion_tree=tree, return_atom_map=True)
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     path = Path(directory) / 'poses.pdbqt'
    ...     _ = path.write_text(text.removeprefix('pdbqt_text:'))
    ...     poses = msm.form.file_pdbqt.read_poses(path, molsys, atom_map)
    >>> poses.structures.coordinates.shape
    (1, 24, 3)

    .. admonition:: User guide

       See :ref:`Tutorial_Read_PDBQT_Poses` for a complete mapped round trip.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_poses import read_poses

    return read_poses(
        item,
        molecular_system,
        atom_map,
        structure_indices,
        missing_atoms,
        return_report,
    )
