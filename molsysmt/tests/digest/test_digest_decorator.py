from molsysmt._private.digestion.digest import digest
import molsysmt.config as config


@digest
def example_function(element, indices, syntaxis):
    return element, indices, syntaxis


@digest
def example_function_no_args_checking(element, indices, syntaxis):
    return element, indices, syntaxis


def test_digest_decorator_with_checking_disabled():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    config.argument_checking = False

    element_digested, indices_digested, syntax_digested = \
        example_function_no_args_checking(element, indices, syntax)

    assert element_digested == element
    assert indices_digested == indices
    assert syntax_digested == syntax


def test_digest_decorator_in_function_without_kwargs():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    config.argument_checking = True
    element_digested, indices_digested, syntax_digested = \
        example_function(element, indices, syntax)

    assert element_digested == "atom"
    assert indices_digested == "all"
    assert syntax_digested == "MolSysMT"


def test_digest_decorator_with_named_arguments():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    config.argument_checking = True
    element_digested, indices_digested, syntax_digested = \
        example_function(element=element,
                         indices=indices,
                         syntaxis=syntax)

    assert element_digested == "atom"
    assert indices_digested == "all"
    assert syntax_digested == "MolSysMT"

    element_digested, indices_digested, syntax_digested = \
        example_function(element,
                         indices=indices,
                         syntaxis=syntax)

    assert element_digested == "atom"
    assert indices_digested == "all"
    assert syntax_digested == "MolSysMT"


@digest
def function_whose_parameters_dont_have_digest_function(element, color):
    return element, color


def test_function_whose_parameters_dont_have_digest_function():

    element = "ATOM"
    color = "BLUE"

    config.argument_checking = True
    element_digested, color_digested = \
        function_whose_parameters_dont_have_digest_function(element, color)

    assert element_digested == "atom"
    assert color_digested == "BLUE"


@digest
def function_with_optional_arguments(indices,
                                     element="system",
                                     syntaxis="molsysmt"):
    config.argument_checking = True
    return indices, element, syntaxis


def test_function_with_optional_arguments():
    indices = "ALL"

    config.argument_checking = True
    indices, element, syntax = \
        function_with_optional_arguments(indices)

    assert indices == "all"
    assert element == "system"
    assert syntax == "molsysmt"


@digest
def example_function_with_kwargs(engine, element, **kwargs):
    if kwargs:
        return engine, element, kwargs
    else:
        return engine, element


@digest
def example_function_with_kwargs_2(element, check=True, **kwargs):
    if kwargs:
        return element, check, kwargs
    else:
        return element, check


def test_digest_decorator_with_kwargs():
    values = example_function_with_kwargs("openmm",
                                          "chain",
                                          name=True,
                                          group_id=True,
                                          molecule_types=True)

    assert len(values) == 3
    keyword_args = values[-1]
    assert values[0] == "OpenMM"
    assert values[1] == "chain"

    assert keyword_args["chain_name"]
    assert keyword_args["group_id"]
    assert keyword_args["molecule_type"]

    config.argument_checking = True
    values = example_function_with_kwargs_2("atom",
                                            n_waters=True,
                                            check=False,
                                            )

    assert len(values) == 3
    keyword_args = values[-1]
    assert values[0] == "atom"
    assert not values[1]
    assert keyword_args["n_waters"]
