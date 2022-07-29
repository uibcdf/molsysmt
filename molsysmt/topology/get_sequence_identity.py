from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_sequence_identity(molecular_system, selection='all', reference_molecular_system=None,
                          reference_selection='all', syntax='MolSysMT', engine='Biopython'):

    from molsysmt.topology.get_sequence_alignment import get_sequence_alignment
    from molsysmt.basic import select

    if engine=='Biopython':

        # This is code from ensembler.modeling.calculate_seq_identity
        # This should be implemented here importing the function but there is a conflict installing
        # ensembler: ensembler is only available for python 2.7
        # (https://github.com/choderalab/ensembler/blob/master/ensembler/modeling.py)

        group_indices = select(molecular_system, element='group', selection=selection)
        reference_group_indices = select(reference_molecular_system, element='group', selection=reference_selection)

        seq, seq_ref = get_sequence_alignment(molecular_system, selection=selection,
                reference_molecular_system=reference_molecular_system,
                reference_selection=reference_selection, syntax=syntax, engine=engine)

        intersect=[]
        intersect_ref=[]

        ii=0
        ii_ref=0

        for res, res_ref in zip(seq, seq_ref):

            if res!='-' and res_ref=='-':
                ii+=1
            elif res=='-' and res_ref!='-':
                ii_ref+=1
            elif res==res_ref:
                if res!='-' and res_ref!='-':
                    intersect.append(group_indices[ii])
                    intersect_ref.append(reference_group_indices[ii_ref])
                    ii+=1
                    ii_ref+=1
            else:
                ii+=1
                ii_ref+=1

    else:

        raise NotImplementedError

    identity = 100.0 * (len(intersect)/len(group_indices))

    return identity, intersect, intersect_ref

