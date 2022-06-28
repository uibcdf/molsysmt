from molsysmt._private.digestion.digest import digest


@digest(check_args=True)
def example_function(element, indices, syntaxis):
    return element, indices, syntaxis


@digest(check_args=False)
def example_function_no_args_checking(element, indices, syntaxis):
    return element, indices, syntaxis


def test_digest_decorator_with_checking_disabled():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    element_digested, indices_digested, syntax_digested = \
        example_function_no_args_checking(element, indices, syntax)

    assert element_digested == element
    assert indices_digested == indices
    assert syntax_digested == syntax


def test_digest_decorator_in_function_without_kwargs():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    element_digested, indices_digested, syntax_digested = \
        example_function(element, indices, syntax)

    assert element_digested == "atom"
    assert indices_digested == "all"
    assert syntax_digested == "MolSysMT"


def test_digest_decorator_with_named_arguments():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

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


@digest(check_args=True)
def function_whose_parameters_dont_have_digest_function(element, color):
    return element, color


def test_function_whose_parameters_dont_have_digest_function():

    element = "ATOM"
    color = "BLUE"

    element_digested, color_digested = \
        function_whose_parameters_dont_have_digest_function(element, color)

    assert element_digested == "atom"
    assert color_digested == "BLUE"


@digest()
def function_with_optional_arguments(indices,
                                     element="system",
                                     syntaxis="molsysmt"):
    return indices, element, syntaxis


def test_function_with_optional_arguments():
    indices = "ALL"

    indices, element, syntax = \
        function_with_optional_arguments(indices)

    assert indices == "all"
    assert element == "system"
    assert syntax == "molsysmt"


@digest(check_args=True, check_kwargs=True)
def example_function_with_kwargs(engine, element, **kwargs):
    if kwargs:
        values = [engine, element]
        return values + [kwarg_name for kwarg_name in kwargs.keys()]
    else:
        return engine, element


def test_digest_decorator_with_kwargs():
    values = example_function_with_kwargs("openmm",
                                          "chain",
                                          name=True,
                                          group_id=True)
    assert len(values) == 4
    assert values[0] == "OpenMM"
    assert values[1] == "chain"
    assert values[2] == "name"
    assert values[3] == "group_id"
