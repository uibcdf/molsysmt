from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from smonitor import signal
from molsysmt.basic import convert
import numpy as np

@signal(tags=['api', 'topology'])
@arg_digest()
def get_sequence_alignment(molecular_system, selection='all', reference_molecular_system=None, reference_selection='all',
                       engine='Biopython', syntax='MolSysMT', prettyprint=False, alignment_index=0, skip_digestion=False):
    """
    Aligning sequences between a query and reference molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    reference_molecular_system : object, default=None
        Argument reference_molecular_system.
    reference_selection : object, default='all'
        Argument reference_selection.
    engine : object, default='Biopython'
        Argument engine.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    prettyprint : object, default=False
        Argument prettyprint.
    alignment_index : object, default=0
        Argument alignment_index.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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
        # Biopython renamed these attributes in recent releases.
        try:
            aligner.end_insertion_score = 0.0
            aligner.end_deletion_score = 0.0
        except Exception:
            aligner.target_end_gap_score = 0.0
            aligner.query_end_gap_score = 0.0
        alignment = aligner.align(tmp_ref_seq, tmp_seq)
        del(aligner, Align, tmp_ref_seq,tmp_seq)

        seq_ref = alignment[alignment_index]._get_row(0)
        seq = alignment[alignment_index]._get_row(1)

    else:

        raise NotImplementedMethodError(caller='molsysmt.topology.get_sequence_alignment')

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
