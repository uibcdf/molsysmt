from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt.basic import convert
import numpy as np

def get_sequence_alignment(molecular_system, selection='all', reference_molecular_system=None, reference_selection=None,
                       engine='Biopython', syntaxis='MolSysMT', prettyprint=False,
                       alignment_index=0, check=True):

    if engine=='Biopython':

        # from ensembler.modeling.align_target_template
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        # See: https://biopython.org/docs/1.75/api/Bio.Align.html#Bio.Align.PairwiseAligner

        from Bio import Align

        tmp_ref_seq=convert(reference_molecular_system, selection=reference_selection,
                syntaxis=syntaxis, to_form='biopython.Seq', check=False)
        tmp_seq=convert(molecular_system, selection=selection, syntaxis=syntaxis,
                to_form='biopython.Seq', check=False)

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

        txt_aln = alignment[alignment_index].format().split('\n')
        seq_ref = txt_aln[0]
        seq = txt_aln[2]

    elif engine=='Modeller':

        raise NotImplementedError

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

