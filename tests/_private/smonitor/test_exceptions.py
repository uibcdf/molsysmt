"""
Unit tests for molsysmt._private.smonitor.exceptions.

Each exception class is instantiated directly so that the __init__ bodies
(branches for optional arguments) are exercised.  This improves coverage
for the exception module which would otherwise only be indirectly tested
when error paths are triggered in integration tests.
"""

import pytest
from molsysmt._private.smonitor.exceptions import (
    ArgumentError,
    ArgumentChoiceError,
    ArgumentLengthError,
    ArgumentConflictError,
    StructuralInconsistencyError,
    InternalAlgorithmError,
    IteratorError,
    LibraryNotFoundError,
    MolecularSystemNeededError,
    MolecularSystemsNeededError,
    NotCompatibleConversionError,
    NotImplementedConversionError,
    NotImplementedIteratorError,
    NotImplementedMethodError,
    NotSupportedFormError,
    NotSupportedSyntaxError,
    NotWithThisFormError,
    FileAlreadyHandledError,
    FileContentError,
    FormatError,
    UnsupportedHeavyOperationError,
    HeavyOutputFailureError,
)


class TestArgumentError:
    def test_basic(self):
        exc = ArgumentError(argument='selection', value='bad_value')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = ArgumentError(argument='selection', value='x', caller='msm.get')
        assert isinstance(exc, Exception)

    def test_with_cause(self):
        cause = ValueError("original error")
        exc = ArgumentError(argument='indices', value=None, cause=cause)
        assert isinstance(exc, Exception)


class TestArgumentChoiceError:
    def test_basic(self):
        exc = ArgumentChoiceError(argument='engine', value='bad', choices=['MolSysMT'])
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = ArgumentChoiceError(argument='engine', value='x', choices=['A', 'B'], caller='msm.get')
        assert isinstance(exc, Exception)


class TestArgumentLengthError:
    def test_basic(self):
        exc = ArgumentLengthError(argument='values', expected=3, actual=5)
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = ArgumentLengthError(argument='values', expected=3, actual=5, caller='msm.set')
        assert isinstance(exc, Exception)


class TestArgumentConflictError:
    def test_basic(self):
        exc = ArgumentConflictError(arg1='selection', arg2='atom_indices', reason='cannot use both')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = ArgumentConflictError(arg1='a', arg2='b', reason='conflict', caller='msm.get')
        assert isinstance(exc, Exception)


class TestStructuralInconsistencyError:
    def test_basic(self):
        exc = StructuralInconsistencyError(reason='n_atoms mismatch')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = StructuralInconsistencyError(reason='mismatch', caller='msm.set')
        assert isinstance(exc, Exception)


class TestInternalAlgorithmError:
    def test_basic(self):
        exc = InternalAlgorithmError(reason='unexpected state')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = InternalAlgorithmError(reason='bad state', caller='kernel')
        assert isinstance(exc, Exception)


class TestIteratorError:
    def test_basic(self):
        exc = IteratorError()
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = IteratorError(caller='molsysmt.iterator')
        assert isinstance(exc, Exception)


class TestLibraryNotFoundError:
    def test_basic(self):
        exc = LibraryNotFoundError(library='rdkit')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = LibraryNotFoundError(library='openmm', caller='msm.convert')
        assert isinstance(exc, Exception)


class TestMolecularSystemNeededError:
    def test_basic(self):
        exc = MolecularSystemNeededError()
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = MolecularSystemNeededError(caller='msm.get')
        assert isinstance(exc, Exception)


class TestMolecularSystemsNeededError:
    def test_basic(self):
        exc = MolecularSystemsNeededError()
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = MolecularSystemsNeededError(caller='msm.compare')
        assert isinstance(exc, Exception)


class TestNotCompatibleConversionError:
    def test_basic(self):
        exc = NotCompatibleConversionError(from_form='molsysmt.MolSys', to_form='rdkit.Mol',
                                            missing_arguments={'atom_indices'})
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotCompatibleConversionError(from_form='A', to_form='B',
                                            missing_arguments={'x'}, caller='convert')
        assert isinstance(exc, Exception)


class TestNotImplementedConversionError:
    def test_basic(self):
        exc = NotImplementedConversionError(from_form='molsysmt.MolSys', to_form='unknown.Form')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotImplementedConversionError(from_form='A', to_form='B', caller='convert')
        assert isinstance(exc, Exception)


class TestNotImplementedIteratorError:
    def test_basic(self):
        exc = NotImplementedIteratorError(form='file:xyz')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotImplementedIteratorError(form='file:xyz', caller='iterate')
        assert isinstance(exc, Exception)


class TestNotImplementedMethodError:
    def test_basic(self):
        exc = NotImplementedMethodError()
        assert isinstance(exc, Exception)

    def test_with_method(self):
        exc = NotImplementedMethodError(method='get_distances', arguments='pbc=True')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotImplementedMethodError(method='foo', arguments='bar', caller='baz')
        assert isinstance(exc, Exception)


class TestNotSupportedFormError:
    def test_basic(self):
        exc = NotSupportedFormError(form='unknown.Form')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotSupportedFormError(form='bad.Form', caller='msm.convert')
        assert isinstance(exc, Exception)


class TestNotSupportedSyntaxError:
    def test_basic(self):
        exc = NotSupportedSyntaxError(syntax='VMD')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotSupportedSyntaxError(syntax='CHARMM', caller='msm.select')
        assert isinstance(exc, Exception)


class TestNotWithThisFormError:
    def test_basic(self):
        exc = NotWithThisFormError()
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = NotWithThisFormError(caller='msm.get')
        assert isinstance(exc, Exception)

    def test_with_form_and_attribute(self):
        exc = NotWithThisFormError(caller='get', form='file:xyz', requested_attribute='velocities')
        assert isinstance(exc, Exception)


class TestFileAlreadyHandledError:
    def test_basic(self):
        exc = FileAlreadyHandledError()
        assert isinstance(exc, Exception)

    def test_with_filename(self):
        exc = FileAlreadyHandledError(filename='test.h5msm')
        assert isinstance(exc, Exception)


class TestFileContentError:
    def test_basic(self):
        exc = FileContentError(reason='unexpected record')
        assert isinstance(exc, Exception)

    def test_with_all_optional(self):
        exc = FileContentError(reason='bad line', caller='parser', record='ATOM', filename='1abc.pdb')
        assert isinstance(exc, Exception)


class TestFormatError:
    def test_basic(self):
        exc = FormatError(reason='invalid format')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = FormatError(reason='bad format', caller='msm.convert')
        assert isinstance(exc, Exception)


class TestUnsupportedHeavyOperationError:
    def test_basic(self):
        exc = UnsupportedHeavyOperationError(operation='get_distances', form='file:xtc',
                                              reason='no coordinates attribute')
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = UnsupportedHeavyOperationError(operation='get_distances', form='file:xtc',
                                              reason='no coords', caller='get_distances')
        assert isinstance(exc, Exception)


class TestHeavyOutputFailureError:
    def test_basic(self):
        exc = HeavyOutputFailureError(reason='out of memory')
        assert isinstance(exc, Exception)

    def test_with_optional_bytes(self):
        exc = HeavyOutputFailureError(reason='oom', predicted_bytes=1000000, available_bytes=500000)
        assert isinstance(exc, Exception)

    def test_with_caller(self):
        exc = HeavyOutputFailureError(reason='oom', caller='get_distances')
        assert isinstance(exc, Exception)
