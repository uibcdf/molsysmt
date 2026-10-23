"""Applying an explicit export naming policy without changing atom identity."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "form"])
@arg_digest()
def project_atom_names(
    molecular_system,
    to_form,
    selection="all",
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Projecting selected atom names into an export format's bounded fields.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form convertible to a native MolSys with atom names.
        The source is unchanged.
    to_form : str
        Export constraint to satisfy: 'file:pdbqt' or 'string:pdbqt_text'. This
        selects the naming policy, not the returned molecular form. No file is written.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms eligible for renaming. Indices are sorted and deduplicated; the
        returned system retains all atoms and structures in their original order.
        The selection must resolve to one flat atom population of plain indices;
        quantity wrappers are rejected, including dimensionless quantities.
    return_report : bool, default=False
        Return a dictionary with molecular_system and a detached correspondence
        report when True; otherwise return the native MolSys alone.
    syntax : str, default='MolSysMT'
        Syntax used for selection.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    molsysmt.MolSys or dict
        Independent native domains with projected labels. Geometry uses protected
        shared blocks until edited. The optional molsysmt.atom_map@1 report
        retains original/output names and IDs, identity index maps and selection
        evidence; it can be passed to compose_atom_maps.

    Raises
    ------
    ArgumentError
        If the target format, selection or report flag is invalid.
    StructuralInconsistencyError
        If topology/group indices are inconsistent or a name namespace
        is exhausted. No partial rename is returned and the source is unchanged.

    Notes
    -----
    The experimental preserve_or_base36 policy retains nonempty printable ASCII
    names of at most four characters, including existing duplicates. Invalid
    selected names receive their first ASCII letter (uppercased), or X, followed
    by a base-36 counter starting at zero. The prefix is lexical, not an element
    assignment. All valid names in the group, including unselected names, are
    reserved before allocation. New names do not collide within that group.
    If any group membership is unknown, all atoms share one conservative
    system-wide collision scope; no group membership is invented.
    Each prefix has 36**3 candidate names; exhaustion raises without truncation.
    Invalid unselected names remain invalid for a later writer to reject.

    For foreign inputs, report source indices/labels refer to the converted
    native atom axis; the input converter retains its own contract.
    IDs, atom order, geometry, chemistry, charge/type values and stored scientific
    provenance are preserved. No names are matched back heuristically: use the
    report's original labels and index maps. Project before assigning charges
    that depend on template names; this tool does not rebind such assignments,
    which may fail their existing validation after renaming. It does not certify
    other PDBQT fields, assign types, prepare chemistry or choose a torsion tree.
    Label projection introduces no third-party scientific method or new credit.

    See Also
    --------
    compose_atom_maps : Compose the rename with preparation and export maps.
    molsysmt.basic.set : Apply explicitly chosen atom names.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys(n_atoms=2)
    >>> msm.set(molsys, atom_name=['H1291', 'H0'])
    >>> result = msm.form.project_atom_names(molsys, to_form='file:pdbqt',
    ...                                      return_report=True)
    >>> result['report']['output_atom_names'].tolist()
    ['H1', 'H0']
    >>> result['report']['source_atom_names'].tolist()
    ['H1291', 'H0']

    .. admonition:: User guide

       See :ref:`Tutorial_Project_Atom_Names` for policy and reversible maps.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.atom_name_projection import project

    return project(molecular_system, to_form, selection, return_report, syntax)
