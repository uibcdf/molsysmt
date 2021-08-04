from molsysmt import convert as _convert
from molsysmt import select as _select
import numpy as np

def sequence_alignment(molecular_system, selection='all', reference_molecular_system=None, reference_selection=None,
                       engine='biopython', syntaxis='MolSysMT', prettyprint=False, prettyprint_alignment_index = 0):

    alignment = None

    if engine=='biopython':

        # from ensembler.modeling.align_target_template
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        from Bio import Align
        tmp_ref_seq=_convert(reference_molecular_system, selection=reference_selection,
                syntaxis=syntaxis, to_form='biopython.Seq')
        tmp_seq=_convert(molecular_system, selection=selection, syntaxis=syntaxis, to_form='biopython.Seq')
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


def structure_alignment(molecular_system, selection_alignment='all', selection_rmsd='backbone',
        frame_indices='all', reference_molecular_system=None, reference_selection_alignment='all',
        reference_selection_rmsd=None, reference_frame_index=0, syntaxis='MolSysMT', parallel=True,
        engine_sequence_alignment = 'biopython', engine_least_rmsd_fit = 'MolSysMT'):

    from .rmsd import least_rmsd_fit as _least_rmsd_fit
    from .multitool import extract as _extract
    from .multitool import select as _select

    if reference_selection_rmsd is None:
        reference_selection_rmsd = selection_rmsd

    if engine_sequence_alignment == 'biopython':

        idty, mask_reference_molecular_system, mask_molecular_system = sequence_identity(molecular_system,
                selection=selection_alignment,
                reference_molecular_system=reference_molecular_system,
                reference_selection=reference_selection_alignment,
                target_intersection_set="atom", engine='biopython')

        molecular_system_selection = _select(molecular_system, selection=selection_rmsd, mask=mask_molecular_system)
        reference_molecular_system_selection = _select(reference_molecular_system, selection=reference_selection_rmsd, mask=mask_reference_molecular_system)

        return _least_rmsd_fit(molecular_system=molecular_system, selection=molecular_system_selection, frame_indices=frame_indices,
                               reference_molecular_system=reference_molecular_system,
                               reference_selection=reference_molecular_system_selection,
                               reference_frame_index=reference_frame_index,
                               engine=engine_least_rmsd_fit, parallel=parallel, syntaxis=syntaxis)

    else:

        raise NotImplementedError

def sequence_identity(molecular_system, selection='all', reference_molecular_system=None, reference_selection=None,
                      syntaxis='MolSysMT', target_intersection_set=None,
                      target_non_intersection_set=None, engine='biopython'):

    if engine=='biopython':

        # This is code from ensembler.modeling.calculate_seq_identity
        # This should be implemented here importing the function but there is a conflict installing
        # ensembler: ensembler is only available for python 2.7
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        aln = sequence_alignment(molecular_system, selection=selection,
                reference_molecular_system=reference_molecular_system,
                reference_selection=reference_selection, syntaxis=syntaxis, engine=engine)

        txt_aln = aln[0].format().split('\n')
        txt_0 = txt_aln[0]
        txt_1 = txt_aln[2]

        len_shorter_seq = min([len(txt_0.replace('-', '')), len(txt_1.replace('-', ''))])
        seq_id = 0
        intersect_1=[]
        intersect_2=[]
        ii_1 = 0
        ii_2 = 0
        for r in range(len(txt_0)):
            res1 = txt_0[r]
            res2 = txt_1[r]
            if res1 == res2:
                seq_id += 1
                intersect_1.append(ii_1)
                intersect_2.append(ii_2)
            if res1 != '-':
                ii_1+=1
            if res2 != '-':
                ii_2+=1
        seq_id = 100 * float(seq_id) / float(len_shorter_seq)
        if target_intersection_set=='group':
            return seq_id, intersect_1, intersect_2
        elif target_intersection_set=='atom':
            from .multitool import get as _get
            set_1 = _get(reference_molecular_system, target='group', indices=intersect_1, atom_indices=True)
            set_1 = np.concatenate(set_1)
            set_2 = _get(molecular_system, target='group', indices=intersect_2, atom_indices=True)
            set_2 = np.concatenate(set_2)
            return seq_id, set_1, set_2
        else:
            return seq_id

    else:

        raise NotImplementedError


