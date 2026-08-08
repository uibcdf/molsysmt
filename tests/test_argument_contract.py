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


# Every function with **kwargs now declares its domain, `convert` included: its keywords
# are resolved from `to_form` through a delegating domain. Anything appearing here admits
# whatever it is given, which is what the contract exists to prevent.
OPEN_WITHOUT_A_DECLARED_DOMAIN = set()


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
    from molsysmt._private.argdigest.function import (
        basic_attribute_functions, basic_convert, get_label)

    declared = {contract.caller for contract in basic_attribute_functions.CONTRACTS}
    declared.add(get_label.contract.caller)
    declared.add(basic_convert.contract.caller)

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


# --- inter-argument rules -------------------------------------------------------------

def test_get_neighbors_refuses_both_search_criteria(alanine_molsys):
    from argdigest import ArgumentConsistencyError

    # `threshold` and `n_neighbors` are alternatives: search within a distance, or search
    # for a count. The rule lived inside the function body and now fails before any work.
    with pytest.raises(ArgumentConsistencyError, match='threshold'):
        msm.structure.get_neighbors(alanine_molsys, threshold='0.5 nm', n_neighbors=3)


def test_get_neighbors_refuses_neither_search_criterion(alanine_molsys):
    from argdigest import MissingArgumentError

    with pytest.raises(MissingArgumentError):
        msm.structure.get_neighbors(alanine_molsys)


@pytest.mark.parametrize('criterion', [{'threshold': '0.5 nm'}, {'n_neighbors': 3}])
def test_get_neighbors_accepts_exactly_one_criterion(alanine_molsys, criterion):
    assert msm.structure.get_neighbors(alanine_molsys, **criterion) is not None


# --- the delegating domain of convert --------------------------------------------------

def test_convert_admits_what_the_target_converter_accepts(alanine_molsys, tmp_path):
    from argdigest import UnknownArgumentError

    # `output_filename` is a parameter of the converter into file:pdb...
    written = msm.convert(alanine_molsys, to_form='file:pdb',
                          output_filename=str(tmp_path / 'x.pdb'))
    assert written

    # ...and of no converter into molsysmt.Topology.
    with pytest.raises(UnknownArgumentError, match='output_filename'):
        msm.convert(alanine_molsys, to_form='molsysmt.Topology', output_filename='x.pdb')


def test_convert_refuses_a_mistyped_converter_keyword(alanine_molsys):
    from argdigest import UnknownArgumentError

    with pytest.raises(UnknownArgumentError, match='output_filenam'):
        msm.convert(alanine_molsys, to_form='file:pdb', output_filenam='x.pdb')


def test_an_unknown_target_form_is_reported_as_such(alanine_molsys):
    from molsysmt._private.smonitor import ArgumentError

    # The domain cannot resolve, so it steps aside and `to_form`'s own digester speaks.
    # Complaining about an unknown argument here would name the wrong problem.
    with pytest.raises(ArgumentError, match='to_form'):
        msm.convert(alanine_molsys, to_form='no.such.form')


def test_the_converter_table_is_plain_data():
    from molsysmt._private.argdigest.domain.converter_arguments import (
        CONVERTER_ARGUMENTS, domain)

    # Written, committed and reviewable in a diff -- not computed while the library runs.
    assert domain.by_value is CONVERTER_ARGUMENTS
    assert len(CONVERTER_ARGUMENTS) > 50
    assert 'output_filename' in CONVERTER_ARGUMENTS['file:pdb']
    assert 'output_filename' not in CONVERTER_ARGUMENTS['molsysmt.Topology']


def test_the_converter_table_still_matches_the_converters():
    """The written table is the contract; this is what stops it drifting from the code.

    Add a keyword to a converter and the table goes stale in a way nothing else notices:
    `convert` keeps refusing a keyword that is now valid, and blames the caller. Change a
    signature so it cannot be read and the names it declared leave the table entirely.
    Either way the fix is mechanical -- regenerate and review the diff -- so the failure
    says exactly that.
    """

    import importlib.util

    spec = importlib.util.spec_from_file_location(
        'generate_converter_arguments',
        'devtools/scripts/generate_converter_arguments.py')
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)

    derived, unreadable = generator.derive()

    assert not unreadable, 'conversion edges with an unreadable signature:\n' + '\n'.join(
        f'{from_form} -> {to_form}: {kind}: {message}'
        for from_form, to_form, kind, message in unreadable)

    from molsysmt._private.argdigest.domain.converter_arguments import CONVERTER_ARGUMENTS

    assert CONVERTER_ARGUMENTS == derived, (
        'the committed table no longer matches the converters. Run:\n'
        '    python devtools/scripts/generate_converter_arguments.py --write')
