from molsysmt._private.exceptions.not_implemented_errors import MolSysNotImplementedError, NotImplementedConversionError
import pytest


def raise_error(error):
    raise error


def raise_error_with_argument(error, *args):
    raise error(*args)


def test_not_implemented_error():
    with pytest.raises(MolSysNotImplementedError) as exc_info:
        raise_error(MolSysNotImplementedError)

    message = (
        "Error in test_not_implemented_error. "
        "The method has not been implemented yet. "
        f" Check  for more information. "
        f"Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for its implementation."
    )
    assert message == str(exc_info.value)


def test_not_implemented_conversion_error():

    with pytest.raises(NotImplementedConversionError) as exc_info:
        raise_error_with_argument(NotImplementedConversionError, "bar", "foo")

    message = (
        "Error in raise_error_with_argument. "
        "Error in conversion from bar to foo"
        "The method has not been implemented yet. "
        f" Check  for more information. "
        f"Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for its implementation."
    )
    assert message == str(exc_info.value)
