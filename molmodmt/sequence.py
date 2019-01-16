from molmodmt import convert as _convert

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

def sequence_identity(ref_item=None, item=None, engine='biopython', **kwards):

    if engine=='biopython':

        from ensembler.modeling import calculate_seq_identity as _ensembler_seq_identity
        alignment = sequence_alignment(ref_item, item, engine)
        return _ensembler_seq_identity(alignment)

    else:

        raise NotImplementedError


