from molsysmt._private.exceptions.not_implemented_errors import MolSysNotImplementedError
import pytest


def raise_error(error):
    raise error


def test_not_implemented_error():
    with pytest.raises(MolSysNotImplementedError) as exc_info:
        raise_error(MolSysNotImplementedError)

    message = (
        "The method has not been implemented yet. "
        f" Check  for more information. "
        f"Write a new issue in https://github.com/uibcdf/MolSysMT/issues asking for its implementation."
    )
    assert message == str(exc_info.value)


def test_not_implemented_conversion_error():
    pass
