from molsysmt._private.exceptions import caller_name as cn
import pytest


def foo():
    """ Returns its name. """
    return cn.caller_name(skip=1)


def function_that_calls_another_function():
    return foo()


def calls_three_functions():
    return function_that_calls_another_function()


def test_get_caller_name_from_function():
    caller_name = foo()
    assert caller_name == "foo"

    caller_name = function_that_calls_another_function()
    assert caller_name == "foo"

    caller_name = calls_three_functions()
    assert caller_name == "foo"


class Bar:

    def baz(self):
        return cn.caller_name(skip=1)

    def call_foo(self):
        return foo()


def test_get_caller_name_from_class():

    bar = Bar()
    caller = bar.baz()
    assert caller == "baz"

    caller = bar.call_foo()
    assert caller == "foo"


class BaseError(ValueError):
    def __init__(self, skip=2, message=None):
        caller_name = cn.caller_name(skip=skip)

        if message is None:
            message = f"Error in {caller_name}. "

        message += "Check docs for more information. "
        super().__init__(message)


class ReportingCallerError(BaseError):
    """ An error that reports the name of the function or method
        thar raises it.
    """
    def __init__(self, argument):
        caller_name = cn.caller_name(skip=2)
        message = f"Error in {caller_name}. Wrong argument {argument}"
        super().__init__(2, message)


class OtherError(BaseError):
    """ An error that reports the name of the function or method
        thar raises it.
    """
    def __init__(self):
        super().__init__(3, None)


def raise_error_function(num):
    if num == 1:
        raise BaseError
    elif num == 2:
        raise OtherError
    raise ReportingCallerError("num")


def test_get_caller_name_from_function_raising_error():

    with pytest.raises(BaseError) as exc_info:
        raise_error_function(1)

    assert "raise_error_function" in str(exc_info)

    with pytest.raises(OtherError) as exc_info:
        raise_error_function(2)

    assert "raise_error_function" in str(exc_info)

    with pytest.raises(ReportingCallerError) as exc_info:
        raise_error_function(3)

    assert "raise_error_function" in str(exc_info)
    assert "Wrong argument num" in str(exc_info)
