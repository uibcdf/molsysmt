from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import *


def _get_reference_sequence(molecular_system):
    """Try to extract a per-chain reference sequence from the molecular system.

    Supported sources:
    * file:pdb          — SEQRES records parsed by PDBFileHandler
    * file:bcif / gz    — ``_entity_poly_seq`` table from the mmCIF binary container
    * string:pdb_id     — downloads the bcif and uses the same path

    Returns
    -------
    dict or None
        ``{chain_id: [res_name_1, res_name_2, ...]}`` with 3-letter residue codes,
        or ``None`` if no sequence information could be found.
    """
    from molsysmt.basic import get_form, convert

    form = get_form(molecular_system)

    # ── PDB file ──────────────────────────────────────────────────────────────
    if form == 'file:pdb':
        pdb_handler = convert(molecular_system, to_form='molsysmt.PDBFileHandler',
                              skip_digestion=True)
        seqres = pdb_handler.entry.primary_structure.seqres
        if not seqres:
            return None
        result = {}
        for rec in seqres:
            result[rec.chainId] = list(rec.resName)
        return result

    # ── BCIF / BCIF.GZ / PDB-ID → use mmcif DataContainer ───────────────────
    if form in ('file:bcif', 'file:bcif_gz', 'string:pdb_id'):
        if form == 'string:pdb_id':
            # Convert PDB ID → bcif file in memory (temp), then read
            import tempfile, os
            tmp = tempfile.NamedTemporaryFile(suffix='.bcif', delete=False)
            tmp.close()
            try:
                convert(molecular_system, to_form=tmp.name, skip_digestion=True)
                return _get_reference_sequence(tmp.name)
            finally:
                os.unlink(tmp.name)

        from mmcif.io.BinaryCifReader import BinaryCifReader
        reader = BinaryCifReader()
        containers = reader.deserialize(molecular_system)
        if not containers:
            return None
        dc = containers[0]

        poly_seq = dc.getObj('entity_poly_seq')
        poly     = dc.getObj('entity_poly')
        if poly_seq is None or poly is None:
            return None

        # Build entity_id → chain_ids mapping from entity_poly
        entity_to_chains = {}
        strand_col = poly.getAttributeList().index('pdbx_strand_id')
        entity_col  = poly.getAttributeList().index('entity_id')
        for i in range(poly.getRowCount()):
            row = poly.getRow(i)
            eid    = row[entity_col]
            strand = row[strand_col]
            # pdbx_strand_id may be comma-separated (e.g. "A,B")
            for ch in strand.split(','):
                entity_to_chains.setdefault(eid, []).append(ch.strip())

        # Build entity_id → ordered list of mon_id
        e_col   = poly_seq.getAttributeList().index('entity_id')
        mon_col = poly_seq.getAttributeList().index('mon_id')
        num_col = poly_seq.getAttributeList().index('num')
        entity_seqs = {}
        for i in range(poly_seq.getRowCount()):
            row = poly_seq.getRow(i)
            eid     = row[e_col]
            mon_id  = row[mon_col]
            num     = int(row[num_col])
            entity_seqs.setdefault(eid, []).append((num, mon_id))

        # Sort by num (should already be sorted, but be safe)
        for eid in entity_seqs:
            entity_seqs[eid].sort(key=lambda x: x[0])

        # Map chain_id → sequence
        result = {}
        for eid, chain_ids in entity_to_chains.items():
            if eid not in entity_seqs:
                continue
            seq = [mon_id for _, mon_id in entity_seqs[eid]]
            for ch in chain_ids:
                result[ch] = seq
        return result or None

    return None


def _compare_sequences(ref_seq, struct_seq):
    """Return list of (insertion_pos, [missing_res_names]) using SequenceMatcher.

    ``insertion_pos`` is the 0-based index in ``struct_seq`` *before* which the
    missing block should be inserted.  If residues are missing after the last
    structural residue, ``insertion_pos`` equals ``len(struct_seq)``.
    """
    from difflib import SequenceMatcher
    sm = SequenceMatcher(None, ref_seq, struct_seq, autojunk=False)
    missing = []
    for tag, i1, i2, j1, _j2 in sm.get_opcodes():
        if tag == 'delete':
            missing.append((j1, list(ref_seq[i1:i2])))
    return missing


@arg_digest()
def get_missing_residues(molecular_system, sequence=None, selection='all',
                         syntax='MolSysMT', engine='MolSysMT'):
    """
    Identify residues that are missing from a molecular system relative to a reference sequence.

    This function compares the residues present in the molecular system against a
    reference sequence and returns a mapping of insertion positions to the names of the
    residues that are absent.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    sequence : dict or None, default None
        Reference sequence as ``{chain_id: [res_name_1, res_name_2, ...]}``, where
        residue names are 3-letter codes.  When ``None`` (default), the function
        attempts to extract the reference sequence automatically:

        * **file:pdb** — from SEQRES records.
        * **file:bcif / file:bcif_gz** — from the ``_entity_poly_seq`` mmCIF table.
        * **string:pdb_id** — downloads the binary CIF and uses the same path.
        * All other forms — emits a ``UserWarning`` and returns ``{}``.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used to restrict the search to a subset of the system.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'MolSysMT', 'PDBFixer'}, default 'MolSysMT'
        Backend used to detect missing residues.

        * ``'MolSysMT'``: native implementation using ``SequenceMatcher`` to align
          the structural sequence against the reference.  Requires a reference
          sequence (from ``sequence`` or auto-detected).
        * ``'PDBFixer'``: delegates to ``pdbfixer.PDBFixer.findMissingResidues``.
          Ignores the ``sequence`` argument.

    Returns
    -------
    dict
        Dictionary mapping ``(chain_index, insertion_position)`` tuples to lists
        of residue names (str).  ``chain_index`` is the 0-based index of the chain
        in the (sub)system; ``insertion_position`` is the 0-based index within that
        chain's *structural* sequence before which the missing residues should be
        inserted.  For insertions after the last residue of a chain the
        ``insertion_position`` equals the number of residues in that chain.

    Raises
    ------
    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    **engine='MolSysMT' limitations:**
    Only amino-acid and nucleotide chains with a detectable reference sequence are
    analysed.  Non-standard residues in the reference that are absent from the
    structure will be reported as missing; non-standard residues present in the
    structure but absent from the reference will be silently ignored.

    **Post-1.0 roadmap:**
    When ``sequence=None`` and the molecular system has no embedded sequence
    information, a future version will optionally query UniProt or the PDB REST API
    using the entity name or PDB ID.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == 'MolSysMT':

        import warnings
        from molsysmt.basic import get, convert

        # Step 1: extract reference sequence from the *original* form (before conversion)
        ref_sequence = sequence
        if ref_sequence is None:
            ref_sequence = _get_reference_sequence(molecular_system)

        if ref_sequence is None:
            warnings.warn(
                "get_missing_residues(engine='MolSysMT'): no reference sequence "
                "available.  Pass a 'sequence' argument or use a PDB/BCIF input "
                "that contains SEQRES / _entity_poly_seq records.  "
                "Returning empty dict.",
                UserWarning,
                stacklevel=2,
            )
            return output

        # Step 2: work on a native MolSys so all get() queries are guaranteed to work
        native = convert(molecular_system, to_form='molsysmt.MolSys',
                         selection=selection, syntax=syntax, skip_digestion=True)

        chain_indices = get(native, element='chain', chain_index=True, skip_digestion=True)
        chain_ids     = get(native, element='chain', chain_id=True,    skip_digestion=True)

        for chain_idx, chain_id in zip(chain_indices, chain_ids):
            if chain_id not in ref_sequence:
                continue

            ref_seq    = ref_sequence[chain_id]
            struct_seq = get(native, element='group',
                             selection=f'chain_index=={chain_idx}',
                             group_name=True, skip_digestion=True)

            if not struct_seq:
                continue

            for insertion_pos, missing_names in _compare_sequences(ref_seq, struct_seq):
                output[(int(chain_idx), insertion_pos)] = missing_names

    elif engine == 'PDBFixer':

        from molsysmt.basic import convert, select

        temp_molecular_system = convert(molecular_system, to_form='pdbfixer.PDBFixer',
                                        selection=selection, syntax=syntax)
        temp_molecular_system.findMissingResidues()

        for (chain_index, insertion_position), residue_names in \
                temp_molecular_system.missingResidues.items():
            output[(chain_index, insertion_position)] = residue_names

    else:

        raise NotImplementedMethodError

    return output
