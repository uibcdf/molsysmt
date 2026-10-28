from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all


@arg_digest(form="file:fasta")
@dep_digest("Bio")
def to_molsysmt_Topology(
    item, atom_indices="all", skip_digestion=False, *, structure_indices="all"
):
    """Converting FASTA sequence occurrences to a topology without synthetic atoms.

    Parameters
    ----------
    item : str or pathlib.Path
        Amino-acid FASTA file. Its existing optional Biopython reader supplies normalized
        sequence text, record IDs and complete descriptions. Use read_records
        separately when original text/normalization evidence is required.
    atom_indices : str, default='all'
        Only 'all' is accepted. Sequence-only conversion no longer constructs
        representative CA atoms and therefore has no selectable atomic axis.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : str, default='all'
        Only 'all' is accepted; FASTA records are not coordinate structures.

    Returns
    -------
    molsysmt.Topology
        Native groups and group-to-molecule membership, with one declared
        molecule/entity/chain slot per record, including repeated and empty
        records. IDs are string labels; equal labels or sequences do not merge
        occurrences or certify chemical identity. Atomic inventory, bonds and
        coordinates remain unspecified, with zero stored atom/bond rows.

    Raises
    ------
    ArgumentError
        If atomic indices are requested or the normalized sequence contains
        unsupported symbols, gaps or stops needing explicit interpretation.
    NotWithThisFormError
        If coordinate structures are requested.

    Notes
    -----
    This intentionally replaces the older implicit one-CA-per-position output.
    The existing amino-acid interpretation is retained; alphabet overlap cannot
    disambiguate a nucleotide sequence from a peptide. No nucleotide inference
    or new automatic alphabet-selection policy is introduced.
    Ordered chain/group membership is stored independently of atoms, including
    empty chains. Generated chain IDs follow A through Z, then AA, AB and onward;
    record tokens remain chain/molecule names and full descriptions entity names.
    Native hierarchy queries, selectors and extraction retain those declarations.
    TopologyDict and H5MSM 0.5 preserve the relation. Separate entity slots do not
    infer equality or inequality of molecular identities.
    Stored atom count zero is not a claim of zero physical atoms. Full atomic
    construction must be explicitly requested through an appropriate build tool.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     path = Path(directory) / 'sequences.fasta'
    ...     _ = path.write_text('>first\\nAG\\n>second\\nW\\n', encoding='utf-8')
    ...     topology = msm.convert(str(path), to_form='molsysmt.Topology')
    >>> topology.n_atoms, topology.n_groups, topology.n_molecules
    (0, 3, 2)

    .. admonition:: User guide

       See :ref:`Tutorial_Form_file_fasta` for normalization and represented hierarchy.

    .. versionadded:: 1.0.0
    """
    from Bio import SeqIO

    from molsysmt.form._sequence_topology import group_names, require_no_structures
    from molsysmt.native._sequence_topology import from_group_records

    require_no_structures(structure_indices, caller=__name__, form="file:fasta")
    if not is_all(atom_indices):
        raise ArgumentError(
            "atom_indices",
            value=atom_indices,
            caller=__name__,
            message="Sequence-only topology has no atomic selection axis.",
        )
    records = []
    for record in SeqIO.parse(item, "fasta"):
        records.append(
            {
                "groups": group_names(str(record.seq), 1, caller=__name__),
                "id": record.id,
                "description": record.description,
            }
        )
    return from_group_records(records)
