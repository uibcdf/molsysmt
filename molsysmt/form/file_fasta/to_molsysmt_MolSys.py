from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:fasta")
@dep_digest("Bio")
def to_molsysmt_MolSys(
    item, atom_indices="all", skip_digestion=False, *, structure_indices="all"
):
    """Converting FASTA records to one native system without atomic construction.

    Parameters
    ----------
    item : str or pathlib.Path
        FASTA file. Every record supplies a separate declared molecular occurrence.
    atom_indices : str, default='all'
        Only 'all' is accepted because the source has no atomic inventory.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : str, default='all'
        Only 'all' is accepted because the source has no coordinate structures.

    Returns
    -------
    molsysmt.MolSys
        Independent partial molecular system with the same topology tables as
        the FASTA-to-Topology converter and zero coordinate structures. No CA
        atoms, chemical bonds or positions are inferred. Known atom-free native
        query/extraction limits remain under MolSysMT #518.

    Raises
    ------
    ArgumentError
        If atomic positions or unsupported sequence symbols are requested.
    NotWithThisFormError
        If coordinate structures are requested.

    See Also
    --------
    molsysmt.form.file_fasta.to_molsysmt_Topology.to_molsysmt_Topology
        Converting the same records into their represented group hierarchy.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     path = Path(directory) / 'sequences.fasta'
    ...     _ = path.write_text('>first\\nAG\\n>second\\nW\\n', encoding='utf-8')
    ...     molsys = msm.convert(str(path), to_form='molsysmt.MolSys')
    >>> molsys.topology.n_atoms, molsys.topology.n_groups, molsys.structures.n_structures
    (0, 3, 0)

    .. admonition:: User guide

       See :ref:`Tutorial_Form_file_fasta` for the declared record and group axes.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import MolSys

    from .to_molsysmt_Topology import to_molsysmt_Topology

    topology = to_molsysmt_Topology(
        item, atom_indices=atom_indices, structure_indices=structure_indices
    )
    output = MolSys()
    output.topology = topology
    return output
