from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@signal(tags=["api", "topology"])
@arg_digest()
@dep_digest("Bio")
def get_sequence_identity(
    molecular_system,
    selection="all",
    reference_molecular_system=None,
    reference_selection="all",
    syntax="MolSysMT",
    engine="Biopython",
    skip_digestion=False,
):
    """
    Calculating sequence identity between two molecular systems.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    reference_molecular_system : molecular system or None, default=None
        Reference system. None uses the query system.
    reference_selection : str, list, tuple or numpy.ndarray, default='all'
        Independent reference group selection, using the reference index space.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : str, default='Biopython'
        Global alignment provider with the scoring of get_sequence_alignment.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    float
        Query-normalized sequence identity percentage (0–100): identical aligned
        letters divided by the number of query letters, excluding non-sequence
        groups. This definition can give different percentages when reversed.
    list of int
        Original query group indices for identical aligned letters, preserving
        selected order and repetitions.
    list of int
        Original reference group indices corresponding to the query matches.


    Raises
    ------
    ArgumentError
        If either selection has no sequence letters, contains pre-existing gaps,
        or supplies invalid positions for a sequence-only input.
    NotImplementedMethodError
        If an unsupported engine is requested.


    Notes
    -----
    Molecular inputs contribute amino-acid groups using the same projection as
    native one-letter sequence conversion. Caps, waters, ions and other group
    types contribute neither a letter nor a denominator term. Sequence-only
    inputs retain their supplied characters and source positions.

    Counting is adapted from Ensembler's calculate_seq_identity. MolSysMT
    preserves its query-length normalization; Ensembler instead uses the shorter
    sequence length. Alignment uses Biopython through get_sequence_alignment.
    Optional Ackredit records the adapted reference and executed provider version
    after a successful calculation, without changing the returned tuple.

    See Also
    --------
    get_sequence_alignment
        Aligning query and reference sequence letters.

    References
    ----------
    .. [1] Ensembler modeling.py, revision 264930d28d3d4987c4fc0c03caba6cf0066e12ca.
       https://github.com/choderalab/ensembler/blob/264930d28d3d4987c4fc0c03caba6cf0066e12ca/ensembler/modeling.py

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['pentalanine']['traj_pentalanine.h5msm']
    >>> identity, groups, reference_groups = get_sequence_identity(molsys)
    >>> identity, groups, reference_groups
    (100.0, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])


    .. versionadded:: 1.0.0
    """

    if engine != "Biopython":
        raise NotImplementedMethodError(
            caller="molsysmt.topology.get_sequence_identity"
        )

    from Bio import __version__ as biopython_version
    from Bio.Seq import Seq

    from molsysmt import _ackredit
    from molsysmt.topology.get_sequence_alignment import get_sequence_alignment

    from ._sequence import identity_attribution, sequence_with_groups

    caller = "molsysmt.topology.get_sequence_identity"
    reference = (
        molecular_system
        if reference_molecular_system is None
        else reference_molecular_system
    )
    sequence, group_indices = sequence_with_groups(
        molecular_system, selection, syntax, caller=caller
    )
    reference_sequence, reference_groups = sequence_with_groups(
        reference, reference_selection, syntax, caller=caller
    )
    # Built Seq inputs and default all-selection options satisfy the aligner's
    # boundary. Molecular filtering and source maps have already been resolved.
    aligned, aligned_reference = get_sequence_alignment(
        Seq(sequence),
        reference_molecular_system=Seq(reference_sequence),
        engine=engine,
        skip_digestion=True,
    )
    intersect, intersect_ref = [], []
    query_position = reference_position = 0
    for letter, reference_letter in zip(aligned, aligned_reference, strict=True):
        if letter != "-" and reference_letter != "-" and letter == reference_letter:
            intersect.append(group_indices[query_position])
            intersect_ref.append(reference_groups[reference_position])
        query_position += letter != "-"
        reference_position += reference_letter != "-"
    identity = 100.0 * len(intersect) / len(group_indices)
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider, identity_attribution(biopython_version), caller, contextual=True
        )
    return identity, intersect, intersect_ref
