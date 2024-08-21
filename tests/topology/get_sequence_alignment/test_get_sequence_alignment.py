"""
Unit and regression test for the get_sequence_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
import numpy as np

# Distance between atoms in space and time

def test_get_sequence_alignment_molsysmt_MolSys_1():
    molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
    molsys_2 = msm.convert(systems['T4 lysozyme L99A']['1l17.h5msm'], to_form='molsysmt.MolSys')
    seq, ref_seq = msm.topology.get_sequence_alignment(molsys, selection='molecule_type=="protein"',
                                    reference_molecular_system=molsys_2, reference_selection='molecule_type=="protein"',
                                    prettyprint=False)
    seq_true = 'MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAAAINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYK--'
    ref_seq_true = 'MNVFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAKSELDKAIGRNCNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRCALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL'
    assert (seq==seq_true) and (ref_seq==ref_seq_true)

def test_get_sequence_alignment_molsysmt_MolSys_2(capsys):
    msm.topology.get_sequence_alignment('AALVRDAVR', reference_molecular_system='EAALFNDAVRQ', prettyprint=True)
    captured = capsys.readouterr()
    assert captured.out=='-AAL\x1b[1;31;48mV\x1b[m\x1b[1;31;48mR\x1b[mDAVR-\n\n\x1b[1;34;48mE\x1b[mAAL\x1b[1;31;48mF\x1b[m\x1b[1;31;48mN\x1b[mDAVR\x1b[1;34;48mQ\x1b[m\n'

