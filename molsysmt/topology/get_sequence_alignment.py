from molsysmt.basic import convert
import numpy as np

def get_sequence_alignment(molecular_system, selection='all', reference_molecular_system=None, reference_selection=None,
                       engine='biopython', syntaxis='MolSysMT', prettyprint=False, prettyprint_alignment_index = 0):

    alignment = None

    if engine=='biopython':

        # from ensembler.modeling.align_target_template
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        from Bio import Align
        tmp_ref_seq=convert(reference_molecular_system, selection=reference_selection,
                syntaxis=syntaxis, to_form='biopython.Seq')
        tmp_seq=convert(molecular_system, selection=selection, syntaxis=syntaxis, to_form='biopython.Seq')
        aligner = Align.PairwiseAligner()
        alignment = aligner.align(tmp_ref_seq, tmp_seq)
        del(aligner, Align, tmp_ref_seq,tmp_seq)

    elif engine=='modeller':

        raise NotImplementedError

    else:

        raise NotImplementedError

    if prettyprint:

        textredbold  =  '\033[1;31;48m' # Red bold text
        textbluebold =  '\033[1;34;48m' # Green bold text
        endcolor = '\033[m' # reset color
        # Color guide in: http://ozzmaker.com/add-colour-to-text-in-python/

        seq1 =""
        seq2 =""

        txt_aln = alignment[prettyprint_alignment_index].format().split('\n')
        txt_0 = txt_aln[0]
        txt_1 = txt_aln[2]

        for r in range(len(txt_0)):
            res1 = txt_0[r]
            res2 = txt_1[r]
            if res1 == res2:
                seq1+=res1
                seq2+=res2
            elif res1 == '-':
                seq1+=res1
                seq2+=textbluebold+res2+endcolor
            elif res2 == '-':
                seq1+=textbluebold+res1+endcolor
                seq2+=res2
            else:
                seq1+=textredbold+res1+endcolor
                seq2+=textredbold+res2+endcolor

        print(seq1)
        print()
        print(seq2)

        pass

    else:

        return alignment


