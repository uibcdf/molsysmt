"""Run the public standard-name examples without treating bare None as output."""

import doctest
import inspect

from molsysmt.element.group.amino_acid import get_standard_name


def test_standard_name_examples_execute_exactly_as_documented():
    example = doctest.DocTestParser().get_doctest(
        inspect.getdoc(get_standard_name),
        {"get_standard_name": get_standard_name},
        "native-standard-name",
        None,
        0,
    )
    result = doctest.DocTestRunner().run(example)
    assert result.attempted == 7
    assert result.failed == 0
