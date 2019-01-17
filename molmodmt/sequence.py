from molmodmt import convert as _convert
from molmodmt import select as _select

def sequence_alignment(ref_item=None, item=None, engine='biopython', **kwards):

    if engine=='biopython':

        # from ensembler.modeling.align_target_template
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        from Bio.pairwise2 import align as _biopython_align
        from Bio.SubsMat import MatrixInfo as _biopython_MatrixInfo
        tmp_ref_seq=_convert(ref_item,'biopython.Seq')
        tmp_seq=_convert(item,'biopython.Seq')
        matrix = getattr(_biopython_MatrixInfo,'gonnet')
        gap_open=-10
        gap_extend=-0.5
        alignment = _biopython_align.globalds(tmp_ref_seq, tmp_seq, matrix, gap_open, gap_extend)
        del(_biopython_MatrixInfo,_biopython_align,matrix,gap_open,gap_extend,tmp_ref_seq,tmp_seq)
        return alignment

    elif engine=='modeller':

        raise NotImplementedError

    else:

        raise NotImplementedError

def structure_alignment(ref_item=None, item=None, ref_frame=0, frame='ALL', parallel=False,
                        in_place=False, engine=['biopython','mdtraj'], **kwards):

    from .rmsd import least_rmsd_fit as _least_rmsd_fit

    if type(engine)==list:
        engine_sequence_alignment = engine[0]
        engine_least_rmsd_fit     = engine[1]
    else:
        engine_sequence_alignment = engine
        engine_least_rmsd_fit     = engine

    if engine_sequence_alignment == 'biopython':

        aln = sequence_alignment(ref_item,item,engine='biopython')
        r_in_common=[[],[]]
        r0=0
        r1=0
        for ii in range(len(aln[0][0])):
            if aln[0][0][ii] != '-':
                if aln[0][0][ii] == aln[0][1][ii]:
                    r_in_common[0].append(r0)
                    r_in_common[1].append(r1)
                r0+=1
            if aln[0][1][ii] != '-':
                r1+=1

        ref_item_selection='resid '+' '.join([str(ii) for ii in r_in_common[0]])
        item_selection='resid '+' '.join([str(ii) for ii in r_in_common[1]])

        if engine_least_rmsd_fit == 'mdtraj':

            return _least_rmsd_fit(ref_item, item, ref_item_selection, ref_frame, item_selection,
                                   frame, parallel=parallel, in_place=in_place, engine='mdtraj')
        else:
            raise NotImplementedError

    else:
        raise NotImplementedError

def sequence_identity(ref_item=None, item=None, engine='biopython', **kwards):

    if engine=='biopython':

        # This is code from ensembler.modeling.calculate_seq_identity
        # This should be implemented here importing the function but there is a conflict installing
        # ensembler: ensembler is only available for python 2.7
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        aln = sequence_alignment(ref_item, item, engine)
        len_shorter_seq = min([len(aln[0][0].replace('-', '')), len(aln[0][1].replace('-', ''))])
        seq_id = 0
        for r in range(len(aln[0][0])):
            if aln[0][0][r] == aln[0][1][r]:
                seq_id += 1
        seq_id = 100 * float(seq_id) / float(len_shorter_seq)
        return seq_id

    else:

        raise NotImplementedError


