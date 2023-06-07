"""
Unit and regression test for the get_sequence_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

# Distance between atoms in space and time

def test_get_sequence_alignment_molsysmt_MolSys_1():
    molsys = msm.convert(tests_systems['T4 lysozyme L99A']['181l.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.convert(tests_systems['T4 lysozyme L99A']['1l17.msmpk'], to_form='molsysmt.MolSys')
    seq, ref_seq = msm.topology.get_sequence_alignment(molsys, selection='molecule_type=="protein"',
                                    reference_molecular_system=molsys_2, reference_selection='molecule_type=="protein"',
                                    prettyprint=False)
    seq_true = 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAAAINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYK--'
    ref_seq_true = 'MNVFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNCNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRCALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'
    assert (seq==seq_true) and (ref_seq==ref_seq_true)

