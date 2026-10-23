"""Composing declared atom axes without matching molecules or generating positions."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "basic"])
@arg_digest()
def compose_atom_maps(atom_maps, skip_digestion=False):
    """Composing sequential preparation, projection, export and pose atom maps.

    Parameters
    ----------
    atom_maps : list or tuple of dict
        Nonempty sequence of completed reports in operation order. Supported
        schemas are molsysmt.terminal_attachment@1, hydrogen_addition@1,
        atom_projection@1, atom_export@1, pdbqt_pose_read@1 and atom_map@1.
        Report arrays may be NumPy arrays or JSON-decoded lists. These are
        declared correspondences; no spatial or chemical matching is performed.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    dict
        Detached molsysmt.atom_map@1 record. Direct forward/inverse int64 maps
        use -1 for absent correspondence. A separate representative map tracks
        original atoms merged into surviving atoms, without giving them those
        atoms' coordinates. Outputs with no original atom are explicitly listed.
        Normalized stage maps retain producer metadata and local merge/parent
        evidence. Charge transfers, when present, carry elementary_charge units.

    Raises
    ------
    ArgumentError
        If atom_maps is not a nonempty sequence of dictionaries.
    StructuralInconsistencyError
        If schema, typed axes, counts, inverse maps, merge evidence or available
        adjacent labels/export bindings disagree.

    Notes
    -----
    Preparation-generated atoms never acquire a pre-generation source index.
    For a pose report, the stage input axis is PDBQT written atom order; its
    output is the reader's native order. Include the writer map before that
    stage. Existing atom_map reports may be composed incrementally; their
    normalized stages are flattened and checked against their aggregate maps.
    Source/output counts and available IDs/names are checked between stages;
    agreement is not authentication of common origin. Chemistry/state changes
    between operations are not inferred or compared as atom identity.
    This tool transports correspondence/provenance, not coordinates, a chemical
    state, new charges or structures. It credits no scientific calculation anew.
    Save the original reports for full scientific/preparation evidence. The
    compact result is a sidecar, not a native H5MSM 0.5 domain.

    See Also
    --------
    molsysmt.form.file_pdbqt.read_poses : Read mapped docking pose coordinates.
    molsysmt.build.merge_nonpolar_hydrogens : Obtain a typed projection report.
    molsysmt.build.add_terminal_atoms : Obtain an explicit atom-creation report.

    Examples
    --------
    >>> import molsysmt as msm
    >>> first = dict(schema='molsysmt.atom_map@1', n_source_atoms=2, n_output_atoms=3,
    ...     source_to_output_atom_indices=[0, 1], output_to_source_atom_indices=[0, 1, -1])
    >>> second = dict(schema='molsysmt.atom_map@1', n_source_atoms=3, n_output_atoms=2,
    ...     source_to_output_atom_indices=[1, -1, 0], output_to_source_atom_indices=[2, 0])
    >>> mapped = msm.basic.compose_atom_maps([first, second])
    >>> mapped['output_to_source_atom_indices'].tolist()
    [-1, 0]
    >>> mapped['source_to_output_atom_indices'].tolist()
    [1, -1]

    .. admonition:: User guide

       See :ref:`Tutorial_Compose_Atom_Maps` for generation and merge semantics.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.atom_maps import compose

    return compose(atom_maps)
