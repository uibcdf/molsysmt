from molsysmt._private.digestion.digest import digest


@digest(check_args=True)
def example_function(element, indices, syntaxis):
    return element, indices, syntaxis


@digest(check_args=False)
def example_function_no_args_checking(element, indices, syntaxis):
    return element, indices, syntaxis


def test_digest_decorator_without_checking_args():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    element_digested, indices_digested, syntax_digested = \
        example_function_no_args_checking(element, indices, syntax)

    assert element_digested == element
    assert indices_digested == indices
    assert syntax_digested == syntax


def test_digest_decorator_without_kwargs():
    element = "ATOM"
    indices = "ALL"
    syntax = "molsysmt"

    element_digested, indices_digested, syntax_digested = example_function(element,
                                                                           indices,
                                                                           syntax)
    assert element_digested == "atom"
    assert indices_digested == "all"
    assert syntax_digested == "MolSysMT"


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

