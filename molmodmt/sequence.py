from molmodmt import convert as _convert
from molmodmt import select as _select

def sequence_alignment(ref_item=None, item=None, engine='biopython', prettyprint=False,
                       prettyprint_alignment_index = 0, **kwards):

    alignment = None

    if engine=='biopython':

        # from ensembler.modeling.align_target_template
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        from Bio.pairwise2 import align as _biopython_align
        from Bio.SubsMat import MatrixInfo as _biopython_MatrixInfo
        tmp_ref_seq=_convert(ref_item, to_form='biopython.Seq')
        tmp_seq=_convert(item, to_form='biopython.Seq')
        matrix = getattr(_biopython_MatrixInfo,'gonnet')
        gap_open=-10
        gap_extend=-0.5
        alignment = _biopython_align.globalds(tmp_ref_seq, tmp_seq, matrix, gap_open, gap_extend)
        del(_biopython_MatrixInfo,_biopython_align,matrix,gap_open,gap_extend,tmp_ref_seq,tmp_seq)

    elif engine=='modeller':

        raise NotImplementedError

    else:

        raise NotImplementedError

    if prettyprint:

        textredbold  =  '\033[1;31;48m' # Red bold text
        textbluebold =  '\033[1;34;48m' # Green bold text
        endcolor = '\033[m' # reset color
        # Color guide in: http://ozzmaker.com/add-colour-to-text-in-python/

        aln = alignment
        align = prettyprint_alignment_index
        seq1 =""
        seq2 =""

        for r in range(len(aln[align][0])):
            res1 = aln[align][0][r]
            res2 = aln[align][1][r]
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


def structure_alignment(ref_item=None, item=None,
                        ref_selection_alignment='all', selection_alignment='all',
                        ref_selection_rmsd=None, selection_rmsd='backbone',
                        ref_frame_index=0, frame_indices='all',
                        parallel=True,
                        engine_sequence_alignment = 'biopython',
                        engine_least_rmsd_fit = 'mdtraj',
                        syntaxis='mdtraj'):

    from .rmsd import least_rmsd_fit as _least_rmsd_fit
    from .multitool import extract as _extract
    from .multitool import select as _select

    if ref_selection_rmsd is None:
        ref_selection_rmsd = selection_rmsd

    if engine_sequence_alignment == 'biopython':

        is_all_ref_item = False
        if type(ref_selection_alignment)==int:
            if ref_selection_alignment=='all':
                is_all_ref_item =True

        if is_all_ref_item:
            tmp_ref_item = ref_item
        else:
            atomslist_ref_alignment = _select(ref_item, ref_selection_alignment)
            tmp_ref_item = _extract(ref_item, atomslist_ref_alignment)

        is_all_item = False
        if type(selection_alignment)==int:
            if selection_alignment=='all':
                is_all_item =True

        if is_all_item:
            tmp_item = item
        else:
            atomslist_alignment = _select(item, selection_alignment)
            tmp_item = _extract(item, atomslist_alignment)

        idty, intersection_atoms = sequence_identity(tmp_ref_item,tmp_item,
                                                     intersection_set="atoms", engine='biopython')

        if not is_all_ref_item:
            intersection_atoms[0]=atomslist_ref_alignment[intersection_atoms[0]]

        if not is_all_item:
            intersection_atoms[1]=atomslist_alignment[intersection_atoms[1]]

        is_all_ref_item = False
        if type(ref_selection_rmsd)==int:
            if ref_selection_rmsd=='all':
                is_all_ref_item =True

        is_all_item = False
        if type(selection_rmsd)==int:
            if selection_rmsd=='all':
                is_all_item =True

        if is_all_ref_item:
            ref_item_selection = 'index '+" ".join(map(str,intersection_atoms[0]))
        else:
            ref_item_selection = ref_selection_rmsd+' and index '+\
                    " ".join(map(str,intersection_atoms[0]))

        if is_all_item:
            item_selection = 'index '+" ".join(map(str,intersection_atoms[1]))
        else:
            item_selection = selection_rmsd+' and index '+" ".join(map(str,intersection_atoms[1]))

        if engine_least_rmsd_fit == 'mdtraj':
            return _least_rmsd_fit(ref_item=ref_item, item=item,
                                   ref_selection=ref_item_selection, selection=item_selection,
                                   ref_frame_index=ref_frame_index, frame_indices=frame_indices,
                                   engine=engine_least_rmsd_fit,
                                   parallel=parallel, syntaxis=syntaxis)
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


