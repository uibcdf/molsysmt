"""
Unit and regression test for the get_sequence_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np

# Distance between atoms in space and time

def test_get_sequence_alignment_molsysmt_MolSys_1():
    molsys = msm.demo.t4_lysozyme_l99a.in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys_2 = msm.demo.files['1l17.mmtf']
    molsys_2 = msm.convert(molsys_2, to_form='molsysmt.MolSys')
    seq, ref_seq = msm.topology.get_sequence_alignment(molsys, selection='molecule_type=="protein"',
                                    reference_molecular_system=molsys_2, reference_selection='molecule_type=="protein"',
                                    prettyprint=False)
    seq_true = 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAAAINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYK--'
    ref_seq_true = 'MNVFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNCNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRCALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'
    assert (seq==seq_true) and (ref_seq==ref_seq_true)

