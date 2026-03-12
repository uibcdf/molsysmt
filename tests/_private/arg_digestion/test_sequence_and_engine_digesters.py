import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.chi1 import digest_chi1
from molsysmt._private.arg_digestion.argument.chi2 import digest_chi2
from molsysmt._private.arg_digestion.argument.chi3 import digest_chi3
from molsysmt._private.arg_digestion.argument.chi4 import digest_chi4
from molsysmt._private.arg_digestion.argument.chi5 import digest_chi5
from molsysmt._private.arg_digestion.argument.engine_least_rmsd_fit import digest_engine_least_rmsd_fit
from molsysmt._private.arg_digestion.argument.engine_sequence_alignment import digest_engine_sequence_alignment
from molsysmt._private.arg_digestion.argument.sequence import digest_sequence
from molsysmt._private.arg_digestion.argument.target_sequence import digest_target_sequence
from molsysmt._private.arg_digestion.argument.mutations import digest_mutations


def test_chi_digesters_accept_bool_for_supported_callers():
    callers = [
        'molsysmt.topology.get_dihedral_quartets.get_dihedral_quartets',
        'molsysmt.structure.get_dihedral_angles.get_dihedral_angles',
    ]
    for caller in callers:
        assert digest_chi1(True, caller=caller) is True
        assert digest_chi2(False, caller=caller) is False
        assert digest_chi3(True, caller=caller) is True
        assert digest_chi4(False, caller=caller) is False
        assert digest_chi5(True, caller=caller) is True
    with pytest.raises(ArgumentError):
        digest_chi1(True)


def test_engine_sequence_digesters_accept_supported_engine_names():
    assert digest_engine_least_rmsd_fit('openmm') == 'OpenMM'
    assert digest_engine_sequence_alignment('biopython') == 'Biopython'
    with pytest.raises(ArgumentError):
        digest_engine_least_rmsd_fit('bad-engine')
    with pytest.raises(ArgumentError):
        digest_engine_sequence_alignment('bad-engine')


def test_sequence_and_mutation_digesters_accept_valid_inputs():
    assert digest_sequence('ACDE') == 'ACDE'
    assert digest_target_sequence('WXYZ') == 'WXYZ'
    with pytest.raises(ArgumentError):
        digest_sequence(3)
    with pytest.raises(ArgumentError):
        digest_target_sequence(3)

    caller = 'molsysmt.build.mutate.mutate'
    assert digest_mutations({'A:1': 'GLY'}, caller=caller) == {'A:1': 'GLY'}
    assert digest_mutations('A:1GLY', caller=caller) == ['A:1GLY']
    assert digest_mutations(['A:1GLY'], caller=caller) == ['A:1GLY']
    with pytest.raises(ArgumentError):
        digest_mutations('A:1GLY')
