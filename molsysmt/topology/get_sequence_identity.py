import numpy as np

def get_sequence_identity(molecular_system, selection='all', reference_molecular_system=None, reference_selection=None,
                      syntaxis='MolSysMT', target_intersection_set=None,
                      target_non_intersection_set=None, engine='biopython'):

    from molsysmt.topology.get_sequence_alignment import get_sequence_alignment

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
            from molsysmt.basic import get as _get
            set_1 = _get(reference_molecular_system, target='group', indices=intersect_1, atom_indices=True)
            set_1 = np.concatenate(set_1)
            set_2 = _get(molecular_system, target='group', indices=intersect_2, atom_indices=True)
            set_2 = np.concatenate(set_2)
            return seq_id, set_1, set_2
        else:
            return seq_id

    else:

        raise NotImplementedError


