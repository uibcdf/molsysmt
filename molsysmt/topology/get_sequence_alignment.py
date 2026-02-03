from molsysmt._private.arg_digestion import arg_digest
from molsysmt.basic import convert
import numpy as np

@arg_digest()
def get_sequence_alignment(molecular_system, selection='all', reference_molecular_system=None, reference_selection='all',
                       engine='Biopython', syntax='MolSysMT', prettyprint=False, alignment_index=0, skip_digestion=False):
    """
    Aligning sequences between a query and reference molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Query system providing the sequence to align.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Group-level selection in the query system.
    reference_molecular_system : molecular system, optional
        Reference system to align against.
    reference_selection : str, list, tuple or numpy.ndarray, default 'all'
        Group-level selection in the reference.
    engine : {'Biopython'}, default 'Biopython'
        Alignment engine.
    syntax : str, default 'MolSysMT'
        Selection syntax for string selections.
    prettyprint : bool, default False
        If True, print a colorized alignment; if False, return aligned sequences.
    alignment_index : int, default 0
        Alignment index to return when multiple alignments are produced.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    tuple of str or None
        `(seq, seq_ref)` aligned strings when `prettyprint=False`; otherwise prints and returns `None`.

    Raises
    ------
    NotImplementedError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    if engine=='Biopython':

        # from ensembler.modeling.align_target_template
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        # See: https://biopython.org/docs/1.75/api/Bio.Align.html#Bio.Align.PairwiseAligner

        from Bio import Align

        tmp_ref_seq= convert(reference_molecular_system, to_form='biopython.Seq', selection=reference_selection,
                             syntax=syntax)
        tmp_seq= convert(molecular_system, to_form='biopython.Seq', selection=selection, syntax=syntax)

        aligner = Align.PairwiseAligner()
        aligner.mode = 'global'
        aligner.match_score = 1.0
        aligner.mismatch_score = 0.0
        aligner.open_gap_score = -0.5
        aligner.extend_gap_score = -0.1
        aligner.target_end_gap_score = 0.0
        aligner.query_end_gap_score = 0.0
        alignment = aligner.align(tmp_ref_seq, tmp_seq)
        del(aligner, Align, tmp_ref_seq,tmp_seq)

        seq_ref = alignment[alignment_index]._get_row(0)
        seq = alignment[alignment_index]._get_row(1)

    else:

        raise NotImplementedError

    if prettyprint:

        textredbold  =  '\033[1;31;48m' # Red bold text
        textbluebold =  '\033[1;34;48m' # Green bold text
        endcolor = '\033[m' # reset color
        # Color guide in: http://ozzmaker.com/add-colour-to-text-in-python/

        pptxt = ''
        pptxt_ref = ''

        for res, res_ref in zip(seq, seq_ref):
            if res == res_ref:
                pptxt+=res
                pptxt_ref+=res_ref
            elif (res == '-' and res_ref != '-'):
                pptxt+=res
                pptxt_ref+=textbluebold+res_ref+endcolor
            elif (res_ref == '-' and res != '-'):
                pptxt+=textbluebold+res+endcolor
                pptxt_ref+=res_ref
            else:
                pptxt+=textredbold+res+endcolor
                pptxt_ref+=textredbold+res_ref+endcolor

        print(pptxt)
        print()
        print(pptxt_ref)

        pass

    else:

        return seq, seq_ref
