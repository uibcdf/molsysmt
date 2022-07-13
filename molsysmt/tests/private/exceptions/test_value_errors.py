import pytest
from molsysmt._private.exceptions.value_errors import *


def raise_error(error):
    raise error


def raise_error_with_argument(error, argument):
    raise error(argument)


@pytest.fixture
def base_error_msg():
    return ("Check  for more information. "
            "If you still need help, open a new issue in https://github.com/uibcdf/MolSysMT/issues."
            )


def test_molsys_value_error(base_error_msg):
    with pytest.raises(MolSysValueError) as exc_info:
        raise_error(MolSysValueError)

    msg = "Error in test_molsys_value_error. "
    msg += base_error_msg
    assert msg == str(exc_info.value)


def test_raise_not_with_this_molecular_system(base_error_msg):
    with pytest.raises(NotWithThisMolecularSystemError) as exc_info:
        raise_error(NotWithThisMolecularSystemError)

    msg = "Error in raise_error. "
    msg += "This method can not be applied over this molecular system. "
    msg += base_error_msg
    assert msg == str(exc_info.value)


def test_multiple_molecular_systems(base_error_msg):
    with pytest.raises(MultipleMolecularSystemsNeededError) as exc_info:
        raise_error(MultipleMolecularSystemsNeededError)

    msg = "Error in raise_error. "
    msg += ('This method works only over a single molecular system. '
            'But multiple molecular systems are provided. ')
    msg += base_error_msg
    assert msg == str(exc_info.value)


def test_not_supported_form(base_error_msg):
    with pytest.raises(NotSupportedFormError) as exc_info:
        raise_error_with_argument(NotSupportedFormError, type("hello"))

    msg = "Error in raise_error_with_argument. "
    msg += "The input molecular system or item has a not supported form: <class 'str'> "
    msg += base_error_msg
    assert msg == str(exc_info.value)


def test_not_with_this_form(base_error_msg):
    with pytest.raises(NotWithThisFormError) as exc_info:
        raise_error_with_argument(NotWithThisFormError, type("hello"))

    msg = "Error in raise_error_with_argument. "
    msg += "Invalid form: <class 'str'> "
    msg += base_error_msg
    assert msg == str(exc_info.value)


def test_wrong_get_argument(base_error_msg):
    with pytest.raises(WrongGetArgumentError) as exc_info:
        raise_error_with_argument(WrongGetArgumentError, "hello")

    msg = "Error in raise_error_with_argument. "
    msg += "The get method was invoked with not valid input argument: \"hello\""
    msg += base_error_msg
    assert msg == str(exc_info.value)
