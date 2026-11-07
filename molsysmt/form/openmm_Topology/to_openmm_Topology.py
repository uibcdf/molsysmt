from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Topology")
def to_openmm_Topology(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Converting from openmm.Topology to openmm.Topology.


    Parameters
    ----------
    item : openmm.Topology
        Source topology, which is left unchanged.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices to retain in source order, coalescing repeated positions.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Unused compatibility argument: this form has no coordinate structures.
    copy_if_all : bool, default=True
        Whether an unrestricted atom selection returns an independent copy.
        Explicit atom subsets always return an independent topology.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Topology retaining labels, insertion codes, known and unknown formal
        charges, remapped bond type/order and periodic box vectors.

    Notes
    -----
    Conversion delegates to the form's metadata-preserving extractor. Full
    copies retain empty groups and chains; atom subsets omit empty parents.

    See Also
    --------
    molsysmt.form.openmm_Topology.extract
        Extracting with the same source-order, metadata and copy policy.

    .. admonition:: User guide

       See :ref:`Tutorial_Form_openmm_Topology` and :ref:`Tutorial_Convert`.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )
