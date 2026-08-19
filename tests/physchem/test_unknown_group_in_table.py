"""An unparameterised residue must say what it is and what to do about it.

Guard for `uibcdf/molsysmt#179`. A residue absent from a per-residue property table
aborted with a bare `KeyError` carrying only the three-letter code — no function, no
table, no remedy. It read as an internal defect rather than as a system the caller has
to decide about, and a bare `KeyError` gives nothing to search for.

Raising is not the defect and must not be undone. The module docstring of
`physchem/groups/_lookup.py` states the intent: dummy residues resolve to neutral, and
`genuine unknown residues still raise so real gaps are not masked`. Reading a missing
parameter as a neutral value would be the worse failure, so these tests pin the raising
behaviour as firmly as the message.
"""

import pytest

from molsysmt._private.smonitor import UnknownGroupInTableError
from molsysmt.physchem.groups._lookup import NEUTRAL_GROUP_NAMES, group_table_value

VALUES = {'ALA': 0.0, 'ASP': -1.0, 'LYS': 1.0}


def test_an_unknown_residue_still_raises():
    """The strictness is the point; only the diagnostic was wrong."""
    with pytest.raises(UnknownGroupInTableError):
        group_table_value(VALUES, 'HED', table='charge',
                          caller='molsysmt.physchem.get_charge')


def test_the_failure_names_the_residue_the_table_the_caller_and_the_remedy():
    with pytest.raises(UnknownGroupInTableError) as failure:
        group_table_value(VALUES, 'HED', table='charge',
                          caller='molsysmt.physchem.get_charge')

    reported = str(failure.value)
    assert 'HED' in reported
    assert 'charge' in reported, 'which table has no entry'
    assert 'molsysmt.physchem.get_charge' in reported, 'which function could not proceed'
    assert 'Remove' in reported, 'what the caller can do about it'


def test_it_is_still_a_key_error():
    """Code written against the previous bare `raise` must keep catching it."""
    with pytest.raises(KeyError):
        group_table_value(VALUES, 'HED', table='charge')


def test_the_message_is_not_wrapped_in_quotes():
    """This is what the base order buys, and it is easy to lose by reordering them.

    `KeyError.__str__` wraps its argument in quotes — the very thing that made the old
    failure unreadable. Keeping `KeyError` in the bases *and* a readable message works
    only while the catalog base comes first, so both halves are asserted rather than
    left to a comment.
    """
    with pytest.raises(UnknownGroupInTableError) as failure:
        group_table_value(VALUES, 'HED', table='charge')

    reported = str(failure.value)
    assert not reported.startswith(('"', "'"))
    assert reported.startswith('Residue')


@pytest.mark.parametrize('group_name', sorted(NEUTRAL_GROUP_NAMES))
def test_dummy_residues_are_still_neutral(group_name):
    """The tolerance this module was written for must survive the change."""
    assert group_table_value(VALUES, group_name, table='charge') == 0.0
    assert group_table_value(VALUES, group_name, neutral=7.0, table='charge') == 7.0


@pytest.mark.parametrize(('group_name', 'expected'), [('ALA', 0.0), ('ASP', -1.0), ('LYS', 1.0)])
def test_known_residues_are_unaffected(group_name, expected):
    assert group_table_value(VALUES, group_name, table='charge') == expected


def test_lookup_is_still_case_insensitive():
    assert group_table_value(VALUES, 'asp', table='charge') == -1.0
