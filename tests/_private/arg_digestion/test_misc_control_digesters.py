import pytest

from molsysmt._private.arg_digestion.argument.chunk import digest_chunk
from molsysmt._private.arg_digestion.argument.start import digest_start
from molsysmt._private.arg_digestion.argument.stop import digest_stop
from molsysmt._private.arg_digestion.argument.step import digest_step
from molsysmt._private.arg_digestion.argument.progress_bar import digest_progress_bar
from molsysmt._private.arg_digestion.argument.prettyprint import digest_prettyprint
from molsysmt._private.arg_digestion.argument.report import digest_report
from molsysmt._private.arg_digestion.argument.verbose import digest_verbose
from molsysmt._private.smonitor import ArgumentError


def test_misc_control_digesters():
    assert digest_chunk(10) == 10
    assert digest_start(0) == 0
    assert digest_stop(None) is None
    assert digest_stop(5) == 5
    assert digest_step(2) == 2
    assert digest_progress_bar(True) is True
    assert digest_prettyprint(True, caller='molsysmt.topology.get_sequence_alignment.get_sequence_alignment') is True
    assert digest_report(False, caller='molsysmt.basic.compare.compare') is False
    assert digest_verbose(True) is True

    with pytest.raises(ArgumentError):
        digest_chunk('10')
    with pytest.raises(ArgumentError):
        digest_progress_bar('yes')
    with pytest.raises(ArgumentError):
        digest_verbose('yes')
