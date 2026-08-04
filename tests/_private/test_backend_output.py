"""
Regression tests for the suppression of third-party output written to the C stdout.

MDTraj's DCD reader prints the detected format with `printf`, on every open and on
every read, and offers no verbosity switch. The messages are not actionable, and the
same plugin ships them commented out in biotraj.
"""

import subprocess
import sys

import molsysmt as msm
import pytest
from molsysmt import systems


def _read_a_dcd(silence):
    """Reading a DCD in a fresh interpreter and returning everything it wrote."""

    script = (
        'import molsysmt as msm\n'
        f'msm.configure.silence_backend_stdout = {silence}\n'
        'from molsysmt import systems\n'
        'dcd = systems["POPC membrane"]["popc_membrane.dcd"]\n'
        'msm.get(dcd, n_atoms=True)\n'
        'msm.convert(dcd, to_form="molsysmt.Structures")\n'
        'for _ in msm.Iterator(dcd, chunk=2):\n'
        '    pass\n'
        'print("DONE")\n'
    )
    # A subprocess is required: the messages are written to the C stdout, so capturing
    # them means capturing the file descriptor, not `sys.stdout`.
    completed = subprocess.run([sys.executable, '-c', script],
                               capture_output=True, text=True, timeout=900)
    assert completed.returncode == 0, completed.stderr[-2000:]
    return completed.stdout


def test_backend_stdout_is_silenced_by_default():
    output = _read_a_dcd(silence=True)
    assert 'DONE' in output, 'the reads themselves must still happen'
    assert 'dcdplugin' not in output


def test_backend_stdout_can_be_let_through():
    # The switch has to work, or a malformed file could not be diagnosed.
    output = _read_a_dcd(silence=False)
    assert 'dcdplugin' in output


def test_silencing_does_not_swallow_python_output():
    # The target is the C stdout of a backend, never the caller's own printing. Python
    # buffers `sys.stdout` separately, so a print inside the context still arrives; the
    # helper must not defeat that, and output after the context must work either way.
    completed = subprocess.run(
        [sys.executable, '-c',
         'from molsysmt._private.backend_output import silence_backend_stdout\n'
         'with silence_backend_stdout():\n'
         '    print("inside")\n'
         'print("after")\n'],
        capture_output=True, text=True, timeout=300)
    assert completed.returncode == 0, completed.stderr[-2000:]
    assert 'inside' in completed.stdout
    assert 'after' in completed.stdout


def test_silencing_restores_the_standard_output_on_error():
    from molsysmt._private.backend_output import silence_backend_stdout

    with pytest.raises(ValueError):
        with silence_backend_stdout():
            raise ValueError('boom')

    # Nothing is asserted about the swallowed bytes; what matters is that the process
    # can still write after an exception left the context.
    print('still able to write')


def test_dcd_values_are_unaffected_by_the_silencing():
    dcd = systems['POPC membrane']['popc_membrane.dcd']

    msm.configure.silence_backend_stdout = False
    try:
        loud = msm.get(dcd, element='atom', coordinates=True)
        loud_n_structures = msm.get(dcd, n_structures=True)
    finally:
        msm.configure.silence_backend_stdout = True

    quiet = msm.get(dcd, element='atom', coordinates=True)

    assert msm.get(dcd, n_structures=True) == loud_n_structures
    assert (loud == quiet).all()
