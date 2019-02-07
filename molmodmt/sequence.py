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

def structure_alignment(ref_item=None, item=None, ref_selection_alignment='All',
                        ref_selection_rmsd=None, ref_frame=0,
                        selection_alignment='All', selection_rmsd='backbone', frame='ALL', parallel=False,
                        in_place=False, engine=['biopython','mdtraj'], **kwards):

    from .rmsd import least_rmsd_fit as _least_rmsd_fit

    if type(engine)==list:
        engine_sequence_alignment = engine[0]
        engine_least_rmsd_fit     = engine[1]
    else:
        engine_sequence_alignment = engine
        engine_least_rmsd_fit     = engine

    if engine_sequence_alignment == 'biopython':

        if ref_selection_alignment not in ['All', 'ALL', 'all']:
            from .multitool import extract as _extract
            tmp_ref_item = _extract(ref_item, ref_selection_alignment)
        else:
            tmp_ref_item = ref_item

        if selection_alignment not in ['All', 'ALL', 'all']:
            from .multitool import extract as _extract
            tmp_item = _extract(item, selection_alignment)
        else:
            tmp_item = item

        idty, intersection_residues = sequence_identity(tmp_ref_item,tmp_item,
                                                     intersection_set="residues", engine='biopython')

        if selection_rmsd in ['All', 'ALL', 'all']:
            ref_item_selection = 'residue '+" ".join(map(str,intersection_residues[0]))
            item_selection = 'residue '+" ".join(map(str,intersection_residues[1]))
        else:
            ref_item_selection = 'residue '+" ".join(map(str,intersection_residues[0]))
            item_selection = 'residue '+" ".join(map(str,intersection_residues[1]))

        if engine_least_rmsd_fit == 'mdtraj':

            return _least_rmsd_fit(ref_item, item, ref_item_selection, ref_frame, item_selection,
                                   frame, parallel=parallel, in_place=in_place, engine='mdtraj')
        else:
            raise NotImplementedError

    else:
        raise NotImplementedError

def sequence_identity(ref_item=None, item=None, intersection_set=None, engine='biopython', **kwards):

    if engine=='biopython':

        # This is code from ensembler.modeling.calculate_seq_identity
        # This should be implemented here importing the function but there is a conflict installing
        # ensembler: ensembler is only available for python 2.7
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        aln = sequence_alignment(ref_item, item, engine)
        len_shorter_seq = min([len(aln[0][0].replace('-', '')), len(aln[0][1].replace('-', ''))])
        seq_id = 0
        intersect_1=[]
        intersect_2=[]
        ii_1 = 0
        ii_2 = 0
        for r in range(len(aln[0][0])):
            res1 = aln[0][0][r]
            res2 = aln[0][1][r]
            if res1 == res2:
                seq_id += 1
                intersect_1.append(ii_1)
                intersect_2.append(ii_2)
            if res1 != '-':
                ii_1+=1
            if res2 != '-':
                ii_2+=1
        seq_id = 100 * float(seq_id) / float(len_shorter_seq)
        if intersection_set=='residues':
            from .multitool import convert as _convert
            tmp_item = _convert(ref_item).topology
            set_1 = [tmp_item.residue(ii).resSeq for ii in intersect_1]
            tmp_item = _convert(item).topology
            set_2 = [tmp_item.residue(ii).resSeq for ii in intersect_2]
            del(_convert,tmp_item)
            return seq_id, [set_1, set_2]
        elif intersection_set=='atoms':
            from .multitool import convert as _convert
            set_1 = []
            tmp_item = _convert(ref_item).topology
            for tmp_residue in [tmp_item.residue(ii) for ii in intersect_1]:
                for tmp_atom in tmp_residue.atoms:
                    set_1.append(tmp_atom.index)
            tmp_item = _convert(item).topology
            set_2 = []
            for tmp_residue in [tmp_item.residue(ii) for ii in intersect_2]:
                for tmp_atom in tmp_residue.atoms:
                    set_2.append(tmp_atom.index)
            del(_convert,tmp_item,tmp_residue,tmp_atom)
            return seq_id, [set_1, set_2]
        else:
            return seq_id

    else:

        raise NotImplementedError


