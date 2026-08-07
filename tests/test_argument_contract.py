"""
Every public function is held to a declared argument contract.

A mistyped keyword used to be discarded in silence, so the call ran with the default and
returned a plausible wrong answer. These are the acceptance tests named in
`devguide/archive/resolved_bugs/public_functions_silently_ignore_unknown_keywords.md`.

The contract of a closed signature is the signature itself, and needs no declaration.
The functions that take attribute names through `**kwargs` declare the `attribute`
domain in `molsysmt/_private/argdigest/function/`.
"""

import inspect

import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt import systems


# `convert` accepts extra keywords whose validity depends on the converter resolved from
# `to_form`, a domain that cannot be decided from the keyword alone. It keeps the
# permissive default, and that gap is recorded in the ArgDigest release notes.
OPEN_WITHOUT_A_DECLARED_DOMAIN = {'convert'}


def _public_callables():
    for name in sorted(dir(msm)):
        if name.startswith('_'):
            continue
        function = getattr(msm, name)
        if not callable(function) or inspect.isclass(function):
            continue
        target = getattr(function, '__wrapped__', function)
        try:
            parameters = inspect.signature(target).parameters
        except (TypeError, ValueError):
            continue
        yield name, target, parameters


def test_the_typo_that_silently_read_a_whole_trajectory_now_raises():
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5msm'],
                         to_form='molsysmt.MolSys')
    good = msm.extract(molsys, selection='all', structure_indices=[0, 1, 2])
    assert msm.get(good, n_structures=True) == 3

    with pytest.raises(UnknownArgumentError, match='structure_indeces'):
        msm.extract(molsys, selection='all', structure_indeces=[0, 1, 2])


def test_the_diagnostic_suggests_the_intended_name(alanine_molsys):
    with pytest.raises(UnknownArgumentError, match='structure_indices'):
        msm.extract(alanine_molsys, selection='all', structure_indeces=[0])


def test_a_closed_function_rejects_a_keyword_it_does_not_declare(alanine_molsys):
    with pytest.raises(UnknownArgumentError, match='bogus'):
        msm.add(alanine_molsys.copy(), alanine_molsys, bogus=1)


def test_an_attribute_that_does_not_exist_is_refused(alanine_molsys):
    with pytest.raises(UnknownArgumentError, match='n_atomss'):
        msm.get(alanine_molsys, n_atomss=True)


@pytest.mark.parametrize('call', [
    lambda molsys: msm.get(molsys, n_atoms=True),
    lambda molsys: msm.get(molsys, element='atom', atom_name=True),
    lambda molsys: msm.contains(molsys, n_waters=0),
    lambda molsys: msm.is_composed_of(molsys, n_peptides=1),
])
def test_the_attribute_domain_still_passes_through(alanine_molsys, call):
    # The fix must not close the door these functions opened on purpose: there are 118
    # attribute names and they can never be signature parameters.
    assert call(alanine_molsys) is not None


def test_no_public_function_raises_an_uncatalogued_error_for_a_typo(alanine_molsys):
    # Before the contract existed, `get` and `contains` leaked a bare KeyError and
    # `convert` a TypeError naming a private converter.
    for call in (lambda: msm.get(alanine_molsys, bogus_attr=True),
                 lambda: msm.contains(alanine_molsys, bogus_attr=True)):
        with pytest.raises(UnknownArgumentError):
            call()


def test_every_open_signature_declares_its_domain():
    from molsysmt._private.argdigest.function import basic_attribute_functions, get_label

    declared = {contract.caller for contract in basic_attribute_functions.CONTRACTS}
    declared.add(get_label.contract.caller)

    undeclared = set()
    for name, target, parameters in _public_callables():
        if not any(p.kind == p.VAR_KEYWORD for p in parameters.values()):
            continue
        caller = f'{target.__module__}.{target.__name__}'
        if caller not in declared:
            undeclared.add(name)

    assert undeclared == OPEN_WITHOUT_A_DECLARED_DOMAIN, (
        'a function with **kwargs and no declared domain admits anything; declare it in '
        'molsysmt/_private/argdigest/function/ or add it to the recorded gap')


def test_the_attribute_domain_points_at_the_catalogue():
    from molsysmt.attribute import attributes
    from molsysmt._private.argdigest.domain.attribute import domain

    # Pointing at the catalogue rather than copying names is what keeps the domain from
    # drifting away from it.
    assert set(domain.known_members()) == set(attributes)
    assert 'n_atoms' in domain
    assert 'not_an_attribute' not in domain
